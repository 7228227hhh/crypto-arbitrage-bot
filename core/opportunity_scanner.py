from typing import Dict,Optional
from data.price_cache import price_cache
from exchanges.binance_client import BinanceClient
from exchanges.price_cache import PriceCache


class OpportunityScanner:
    """负责从缓存读取价格，并且扫描机会"""
    def __init__(self,symbols:List[str],exchange_client,price_cache):
        self.symbols=symbols
        self.exchange=exhcange_client#外部注入
        self.price_cache=price_cache#外部注入
    def scan(self)->Optional[Dict]:
        """扫描套利机会"""
        for symbol in self.symbols:
            price=price_cache.get_latest_price(symbol)
            if price:
                print(f"{symbol}当前的价格{price:.2f}(来自缓存)")
                #TODO:加入价差对比逻辑
        return None
    def check_spread(self,symbol:str,exchange_a:str,exchange_b:str)->Optional[Dict]:
        """交易所简单比价"""
        price_a=exchange_a.fetch_ticker(symbol)
        price_b=exchange_b.fetch_ticker(symbol)
        if not price_a or not price_b:
            return None
        #价差百分比
        spread_pct=abs(price_a-price_b)/price_a*100
        # 扣除手续费后的净利润（假设双边手续费各0.1%）
        fee_pct = 0.2  # 0.1% + 0.1%
        net_profit_pct = spread_pct - fee_pct
        if net_profit_pct > self.min_profit_pct:  # 比如 0.3%
            if price_a < price_b:
                return {"action": "BUY", "exchange": exchange_a, "sell_exchange": exchange_b, "profit": net_profit_pct}
            else:
                return {"action": "BUY", "exchange": exchange_b, "sell_exchange": exchange_a, "profit": net_profit_pct}

            return None