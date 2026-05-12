import binance_client
import exchange_base
from typing import Dict,Optional
from exchanges.binance_client import BinanceClient
import price_cache


class OrderManager:
    #订单执行器,不要写死了交易所
    #初始化
    def __init__(self,client):
        self.client=client
        self.price_cache=price_cache.PriceCache()
        self.order_history=[]
        self.max_reties=3#重试3次
        self.retry_delay=1#每次间隔1s
    def excute_signal(self,signal:Dict)->Optional[Dict]:
        """执行完整的交易信号
        signal格式：{"action"，"symbol","amount"}"""
        action=signal.get("action")
        symbol=signal.get("symbol")
        amount=signal.get("amount")
        #-------------前置检查--------------
        if not all([action,symbol,amount]):
            print("🈲信号缺少字段")
            return None
        #检查余额（暂时用币安的方式，后续等工厂模式更新）
        balance=self.client.fetch_balance()
        quote_asset = symbol.split("/")[1]  # BTC/USDT -> USDT
        base_asset = symbol.split("/")[0]  # BTC/USDT -> BTC

        if action.upper()=="BUY":
            estimated_cost = amount * self.client.fetch_ticker(symbol=symbol)
            if balance<estimated_cost:
                print(f"余额不足，需要{estimated_cost-balance}{quote_asset}")
                return None
        elif action.upper()=="SELL":
            balance=self.client.fetch_balance(params)#这个方法需要补充，前面的币安没有写全
            if amount>balance:
                print(f"余额不足，需要{amount-balance}{base_asset}")
                return None
        #----------执行下单（带重试）-----------
        order = None
        for attempt in range(self.max_reties):
            try:
                print(f"尝试下单({attempt+1}/{self.max_reties}):{action}{amount}{symbol}")
                #order=self.client.create_order()
                order={
                    "order_id": f"sim_{int(time.time())}",
                    "action": action,
                    "symbol": symbol,
                    "amount": amount,
                    "price": self.get_current_price(symbol),
                    "status": "filled",
                    "timestamp": time.time()
                }
                break
            except Exception as e:
                print(f"⚠️ 下单失败 (尝试 {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    print(f"❌ 下单最终失败，已重试 {self.max_retries} 次")
                    return None
        if not order:
            return None
        #---------------后置处理-----------------
        #记录到历史
        self.order_history.append(order)
        print(f"已下单，成功记录为：{order}")
        self.post_process(order)#处理后续任务
        #---------状态跟踪（异步查询）
        self.track_order_status(order.get("order_id"))
        return order
    def track_order_status(self,order_id):
        """后置处理：记录日志、更新统计等"""
        # TODO: 发送通知、更新数据库、触发风控更新
        pass

    def _track_order_status(self, order_id: str):
        """跟踪订单最终状态"""
        # TODO: 轮询或回调检查订单是否最终成交
        # 对于模拟订单，直接标记完成
        pass
















