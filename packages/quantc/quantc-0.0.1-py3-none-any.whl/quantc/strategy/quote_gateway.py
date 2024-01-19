from abc import ABC, abstractmethod

from pandas import DataFrame

from ..common.constant import GlobalIndex
from ..common.data_object import OrderBook


class QuoteGateway(ABC):
    @abstractmethod
    def connect(self, setting: dict) -> None:
        """
        Start gateway connection.

        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Close gateway connection.
        """
        pass

    @abstractmethod
    def subscribe(self, code_list: list, subtype_list=None) -> None:
        """
        Subscribe tick data update.
        """
        pass

    @abstractmethod
    async def get_cur_day_kline(self, code, num) -> DataFrame:
        """
        获取实时日K线
        :param code: 代码
        :param num: 日数量
        :return:日K线DataFrame
        """
        pass

    @abstractmethod
    async def get_cur_index_day_kline(self, code, index=GlobalIndex.USI, num=56) -> DataFrame:
        """
        获取指定指数的日K线
        :param code: 当前标的代码
        :param index 指数代码
        :param num: K线数量
        :return:
        """
        pass

    @abstractmethod
    async def get_lot_size(self, code) -> int:
        """
        获取当前标的的每手股数
        """
        pass

    @abstractmethod
    async def get_order_book(self, code) -> OrderBook:
        pass

    @abstractmethod
    async def is_trading_day(self, market) -> bool:
        pass

    @abstractmethod
    async def is_trading_time(self, market) -> bool:
        pass
