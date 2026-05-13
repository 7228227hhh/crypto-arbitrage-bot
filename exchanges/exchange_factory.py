from distutils.command.install import key
from typing import Dict,Any
from exchange_base import ExchangeBase
from exchanges.binance_client import BinanceClient
from exchanges.coinbase_client import CoinbaseClient
class exchange_factory:
    """交易所工厂"""
    #交易所名称到类的映射
    _exchange_map={
        'binance':BinanceClient,
        'coinbase':CoinbaseClient,
    }
    @classmethod
    def create(cls,exchange_name:str,config:Dict[str,Any]=None) -> ExchangeBase:
        """
         创建交易所实例

         Args:
             exchange_name: 交易所名称，如 "binance", "coinbase"
             config: 可选配置（API Key、Secret等），默认从环境变量读取

         Returns:
             交易所客户端实例

         Raises:
             ValueError: 不支持的交易所名称
         """
        exchange_name = exchange_name.lower()
        if exchange_name not in cls._exchange_map:
            raise ValueError(f"不支持的交易所：{exchange_name}，支持的有：{list(cls._exchange_map.keys())}")
            client_class=cls._exchange_map[exchange_name]
        if config :
            return client_class(**config)
        else:
            return client_class()
    @classmethod
    def get_supported_exchanges(cls) -> List[str]:
        """获取支持的交易所列表"""
        return list(cls._exchange_map.keys())
    @classmethod
    def register(cls, name: str, client_class):
        """动态注册新交易所（用于插件式扩展）"""
        cls._exchange_map[name.lower()] = client_class



