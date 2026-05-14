import time
import threading
from typing import List
from data.price_cache import price_cache
from exchanges.binance_client import BinanceClient
from exchanges.price_cache import PriceCache
import asyncio
import exchange_factory
from pandas.io.formats.format import return_docstring


class PriceMonitor(threading.Thread):

    """获取价格，写入缓存"""
    def __init__(self,symbols:List[str],exchange_factory,price_cache):
        super().__init__()#这行一定要加，因为有父类threding.Thread也需要初始化
        self.symbols=symbols
        self.running=True
        self._thread=None
        self.exchange_factory=exchange_factory
        self.price_cache=price_cache
    def start(self):
        """启动监控（独立线程）"""
        self.running=True
        #这里注意如果是异步定义了一个方法，那么这个方法就必须要用异步方法来启动，不能直接run需要用asyncio.run
        self._thread=threading.Thread(target=self._run_async_loop,daemon=True)#daemon是守护线程参数，设置为true会随着主线程的终止而强行停止
        self._thread.start()
        print(f"关于{self.symbols}的价格监控启动")

    def _run_async_loop(self):
        asyncio.run(self._loop())

    async def get_prices(self):
        tasks=[exchange.fetch_ticker(self.symbols) for exchange in self.exchange_factory._exchange_map.values() ]
        results=await asyncio.gather(*tasks,return_exceptions=True)#这里注意解包的原因是因为避免把列表当成一个参数传入,设置为true避免崩掉
        for result in results:
            if isinstance(result,Exception):#isinstance()用来判断对象的类型是否是什么什么
                continue
            for ticker in result:
                symbol = ticker["symbol"]
                price = ticker["last"]
                if price:
                    self.price_cache.update(symbol,price)
                    print(f"{symbol}:${price:.2f}已经写入缓存")


    async def _loop(self):
            while self.running:
                start_time = time.time()
                await self.get_prices()  # 调用异步方法
                elapsed = time.time() - start_time
                sleep_time = max(0, 1 - elapsed)
                await asyncio.sleep(sleep_time)
            """for symbol in self.symbols:
                try:
                    ticker=self.client.fetch_ticker(symbol=symbol)
                    price=ticker.get("last")
                    if price:
                        price_cache.update(symbol,price)
                    print(f"{symbol}:${price:.2f}当前信息"
                          f""
                          f"已经写入缓存")
                except Exception as e:
                    print(f"获取{symbol}失败：{e}")
                    time.sleep(1)"""
    def stop(self):
        self.running=False
        if self._thread:
            #等待loop线程2秒钟
            self._thread.join(timeout=2)







