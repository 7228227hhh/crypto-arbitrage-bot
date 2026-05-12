#数据缓冲池
import time
from typing import Dict,List,Optional
from collections import deque
class PriceCache:
    def __init__(self,max_history=200):
        #这里需要记住，存放历史数据python里面最好写成字典，因为字典查找复杂度只有O（1），但是列表查找有O（n）
        self.lastest:Dict[str,float]={}
        #历史价格
        self.history:Dict[str,deque]={}
        self.max_history:int=max_history
    # 添加所有的合约信息
    def update(self,symbol:str,price:float):
        #写入最新价格
        self.lastest[symbol]=price
        #保存新来的价格为历史
    if symol not in self.history:
        self.history[symol]=deque(maxlen=self.max_history)
        self.history[symol].append((time.time(),price))
    #供策略调用最新价格
    def get_latest_price(self,symbol:str) ->Optional[float]:
        #这里需要用get方法的原因是避免空值让程序崩溃
        return self.latest.get[symbol]
    def get_history(self,symbol:str,seconds: int=60) -> List[tuple]:
        '''策略调用，获取最近n秒的历史价格'''
        if symbol not in self.history:
            return []
        cutoff=time.time()-seconds
        return [(ts,p) for ts,p in self.history[symbol] if ts >= cutoff ]
    price.cache=PriceCache()



