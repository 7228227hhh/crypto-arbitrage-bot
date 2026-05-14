# exchanges/okx_client.py
import ccxt
from exchanges.exchange_base import ExchangeBase


class OKXClient(ExchangeBase):
    """OKX交易所客户端

    testnet=True: 使用模拟盘
    testnet=False: 使用实盘
    """

    def __init__(self, api_key: str, secret_key: str, password: str = None,
                 enableRateLimit: bool = True, testnet: bool = True) -> None:
        """
        初始化 OKX 客户端

        注意：OKX 需要额外的 password（交易密码/API 密码）
        """
        exchange_config = {
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': enableRateLimit,
        }

        # OKX 特有：API 密码
        if password:
            exchange_config['password'] = password

        self.exchange = ccxt.okx(exchange_config)

        if testnet:
            # OKX 模拟盘模式
            self.exchange.set_sandbox_mode(True)
            print("OKX：正在使用模拟盘模式")
        else:
            print("OKX：正在使用实盘模式")

    '''把价格获取方式改成异步，并且可以接受列表参数'''
    def fetch_single(self,symbol):
        result=self.exchange.fetch_ticker(symbol)
        return result
    async def fetch_ticker(self,symbols):
        symbols=symbol if isinstance(symbol, list) else [symbol]
        tasks=[asyncio.to_thread(self.fetch_single,s) for s in symbols]
        results=await asyncio.gather(*tasks,return_exceptions=True)
        return results



    '''def fetch_ticker(self, symbol: str):
        """
        获取当前价格（返回最新价）

        参数：
        symbol：交易对，格式如 "BTC/USDT"

        返回：
        float: 当前价格
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker['last']
        except Exception as e:
            print(f"OKX 价格获取失败: {e}")
            return None'''

    def create_order(self, symbol: str, order_type: str, side: str,
                     amount: float, price: float = None, params: dict = None):
        """
        创建订单

        参数：
        symbol: 交易对，如 "BTC/USDT"
        order_type: 订单类型，'limit' 或 'market'
        side: 交易方向，'buy' 或 'sell'
        amount: 数量
        price: 限价单价格（市价单不需要）
        params: 扩展参数（如 {'reduceOnly': True} 用于减仓）

        返回：
        dict: 订单详情
        """
        if params is None:
            params = {}

        try:
            order = self.exchange.create_order(
                symbol, order_type, side, amount, price, params
            )
            print(f"✅ OKX {symbol} {side} {amount} 下单成功!")
            return order
        except Exception as e:
            print(f"❌ OKX {symbol} {side} 下单失败: {e}")
            return None

    def fetch_balance(self, params: dict = None):
        """
        查询账户余额

        参数：
        params: 扩展参数，如 {'type': 'trading'} 指定账户类型

        返回：
        dict: 余额，格式：
            {
                'BTC': {'free': 0.1, 'used': 0.0, 'total': 0.1},
                'USDT': {'free': 1000.0, 'used': 0.0, 'total': 1000.0}
            }
        """
        if params is None:
            params = {}

        try:
            balance = self.exchange.fetch_balance(params)
            return balance
        except Exception as e:
            print(f"OKX 查询余额失败: {e}")
            return None

    def fetch_order(self, order_id: str, symbol: str = None, params: dict = None):
        """查询订单状态"""
        if params is None:
            params = {}

        try:
            order = self.exchange.fetch_order(order_id, symbol, params)
            print(f"OKX 订单 {order_id} 状态: {order['status']}")
            return order
        except Exception as e:
            print(f"OKX 查询订单失败: {e}")
            return None

    def fetch_open_orders(self, symbol: str = None, since: int = None,
                          limit: int = None, params: dict = None):
        """查询未成交订单"""
        if params is None:
            params = {}

        try:
            orders = self.exchange.fetch_open_orders(symbol, since, limit, params)
            print(f"OKX 未成交订单数量: {len(orders)}")
            return orders
        except Exception as e:
            print(f"OKX 查询未成交订单失败: {e}")
            return []

    def cancel_order(self, order_id: str, symbol: str = None, params: dict = None):
        """取消订单"""
        if params is None:
            params = {}

        try:
            result = self.exchange.cancel_order(order_id, symbol, params)
            print(f"✅ OKX 订单 {order_id} 取消成功")
            return result
        except Exception as e:
            print(f"❌ OKX 取消订单失败: {e}")
            return None

    def fetch_ohlcv(self, symbol: str, timeframe: str = '1m',
                    since: int = None, limit: int = 100):
        """
        获取K线数据

        参数：
        symbol: 交易对
        timeframe: 时间周期 (1m, 5m, 15m, 1h, 4h, 1d, 1w)
        since: 起始时间戳（毫秒）
        limit: 数量限制

        返回：
        list: K线列表，每根格式 [timestamp, open, high, low, close, volume]
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            return ohlcv
        except Exception as e:
            print(f"OKX 获取K线失败: {e}")
            return []

    def get_websocket_url(self):
        """
        获取 WebSocket URL

        参考: https://www.okx.com/docs-v5/zh/#websocket-api
        """
        return "wss://ws.okx.com:8443/ws/v5/public"