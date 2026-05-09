import ccxt
from .exchange import ExchangeBase
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
    def get_price(self,symbol: str) -> float32:
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




