from abc import ABC, abstractmethod
from pip._internal.cli.spinners import RateLimiter
#写成抽象基类，注意需要参考ccxt的接口命名规范
class ExchangeBase(ABC):
    #--------------必须实现-------------
    @abstractmethod
    def fetch_ticker(self,*args,**kwargs) :
        '''获取实时价格bid,ask'''
        pass
    @abstractmethod
    def create_order(self,*args,**kwargs):
        '''创建订单'''
        pass
    @abstractmethod
    def fetch_balance(self,*args,**kwargs):
        """查询余额"""
        pass
    @abstractmethod
    def fetch_order(self,*args,**kwargs):
        """查询订单状态"""
        pass

    @abstractmethod
    def fetch_open_orders(self,*args,**kwargs):
        """查询未成交订单"""
        pass

    @abstractmethod
    def cancel_order(self,*args,**kwargs)->bool:
        """取消订单"""
        pass

    @abstractmethod
    def get_websocket_url(self)->str:
        """获取websocket地址"""
        pass

#--------------MIXIN增强方法-------------
#--------------订单数据增强-------------
class MarketDataMixin:
    def subscribe_ticker(self,symbol:str,callback):
        '''订阅行情'''
        pass
    def fetch_orderbook(self,symbol:str,depth):
        '''获取订单簿厚度'''
        pass
    def fetch_klines(self,symbol:str,interval:str,limit:int=500):
        '''加载k线'''
        pass
#账户资金拓展
class AccountMixin:
    def fetch_fees(self,symbol:str=None):
        '''查询手续费'''
        pass
    def withdraw(self,asset:str,amount:float,address:str)->bool:
        '''提现'''
        pass
    def fetch_deposit_history(self,asset:str=None):
        '''查询充值情况'''
        pass
#API限频管理
class RateLimitMixin:
    def __init__(self):
        self.rate_limiter=RateLimiter()

    def check_rate_limit(self,endpoint:str):
        '''检查然后等待限频'''
        pass
    '''property是一个内置装饰器，用处在于可以将类的方法变得和类的属性一样，调用的时候不需要带括号，方便重写和审阅'''
    @property
    def rate_limit_per_second(self)->int:
        '''每秒请求限制'''
        return 100


