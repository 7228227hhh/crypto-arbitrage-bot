import ccxt
from exchange_base import ExchangeBase
#接入币安
class BinanceClient(ExchangeBase):
    '''testnet=true:使用测试
         testnet=false:使用实盘'''
    def __init__(self,testnet:bool=True) -> None:
     #需要币安自动限频，避免被封
        self.exchange = ccxt.binance({'enableRateLimit': True})
        if testnet:
         self.exchange.set_sandbox_mode(True)
         print("币安：正在使用测试模式")
        else:
         print("币安：正在使用实盘模式")
    def fetch_ticker(self,symbol: str):
        '''
        获取当前价格（返回最新价）
        参数：
        symbol：交易对
        返回：
        float32:当前价格
        '''
        try:
            tiker=self.exchange.fetch_ticker(symbol)
            return tiker['last'
            ]
        except Exception as e:
            print(f"价格获取失败{e}")
            return None
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
        # TODO: 币安将在2026年4月后更换WebSocket地址，届时需要更新为新架构的URL
        #       新架构地址格式: wss://fstream.binance.com/{public,market,private}
        #       目前暂时使用旧地址保证功能正常
        """获取WebSocket URL"""
        return "wss://stream.binance.com:9443/ws"











