import ccxt
from exchange_base import ExchangeBase
import asyncio
#接入币安
class BinanceClient(ExchangeBase):
    '''testnet=true:使用测试
         testnet=false:使用实盘'''
    def __init__(self,api_key,secret_key,enableRateLimit:bool=True,testnet:bool=True) -> None:
     #需要币安自动限频，避免被封
        exchange_config={
            'apiKey':api_key,
            'secret':secret_key,
            'enableRateLimit':enableRateLimit,
        }
        self.exchange = ccxt.binance(exchange_config)
        if testnet:
         self.exchange.set_sandbox_mode(True)
         print("币安：正在使用测试模式")
        else:
         print("币安：正在使用实盘模式")
    #增加了symbols的调用方式，可以直接传入列表来查询价格
    def _fetch_single(self, symbol):
        """单个获取的实际逻辑"""
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker
#注意，当函数内部使用了await的时候就需要用async来定义，然后会返回一个coroutine(协程）对象，需要用await方法来转化成返回值
    async def fetch_ticker(self, symbol):
        symbols = symbol if isinstance(symbol, list) else [symbol]
        # 把同步函数放到线程池,这里用asyncio.to_thread方法就可以
        tasks = [asyncio.to_thread(self._fetch_single, s) for s in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    def create_order(self,symbol,order_type:str,side:str,amount,price:float=None,params=None):
        """创建订单
        参数：交易对，订单类型（limit or market),交易方向，数量，限价单价格，拓展参数
        返回：订单详情dict"""
        try:
            order=self.exchange.create_order(symbol,order_type,side,amount,price,params)
            print(f"{symbol}-{side}-{order_type}-{amount}下单成功!价格：{price}")
            return order
        except Exception as e:
            print(f"{symbol}-{side}-{order_type}-{amount}下单失败!")
            return None

    def fetch_balance(self, params=None):
        """
        查询账户余额
        参数:
        - params: 扩展参数（可选），如指定账户类型 {'type': 'future'}
        返回:
        - balance dict: 包含 total, free, used 三个子字典
        """
        try:
            balance = self.exchange.fetch_balance(params)
            # 返回格式示例:
            # {
            #   'BTC': {'free': 0.1, 'used': 0.0, 'total': 0.1},
            #   'USDT': {'free': 1000.0, 'used': 0.0, 'total': 1000.0}
            # }
            return balance
        except Exception as e:
            print(f"查询余额失败: {e}")
            return None

    def fetch_order(self, order_id: str, symbol: str = None, params: dict = None):
        """查询订单状态"""
        if params is None:
            params = {}
        try:
            order = self.exchange.fetch_order(order_id, symbol, params)
            print(f"订单 {order_id} 状态: {order['status']}")
            return order
        except Exception as e:
            print(f"查询订单失败: {e}")
            return None

    def fetch_open_orders(self, symbol: str = None, since: int = None, limit: int = None, params: dict = None):
        """查询未成交订单"""
        if params is None:
            params = {}
        try:
            orders = self.exchange.fetch_open_orders(symbol, since, limit, params)
            print(f"未成交订单数量: {len(orders)}")
            return orders
        except Exception as e:
            print(f"查询未成交订单失败: {e}")
            return []

    def cancel_order(self, order_id: str, symbol: str = None, params: dict = None):
        """取消订单"""
        if params is None:
            params = {}
        try:
            result = self.exchange.cancel_order(order_id, symbol, params)
            print(f"✅ 订单 {order_id} 取消成功")
            return result
        except Exception as e:
            print(f"❌ 取消订单失败: {e}")
            return None

    def get_websocket_url(self):
        """
        获取WebSocket URL

        TODO: 2026年4月前需要迁移到新架构
              - 旧地址: wss://stream.binance.com:9443/ws (当前使用)
              - 新地址: wss://fstream.binance.com/{public,market,private}
              参考: https://binance-docs.github.io/apidocs/websocket_api/en/
        """
        # FIXME: 临时使用旧地址，后续需改造
        return "wss://stream.binance.com:9443/ws"
