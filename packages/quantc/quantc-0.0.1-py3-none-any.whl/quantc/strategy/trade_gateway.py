from abc import ABC, abstractmethod
from datetime import datetime

from pandas import DataFrame

from ..common.data_object import AccInfo, Position


class TradeGateway(ABC):
    @abstractmethod
    async def get_position(self, code, acc_id: str, strategy_id: int = None) -> Position:
        pass

    @abstractmethod
    async def get_acc_info(self, acc_id: str) -> AccInfo:
        pass

    # @abstractmethod
    # async def create_acc_info(self, acc_id: str, cash: float) -> AccInfo:
    #     pass

    # @abstractmethod
    # def get_cash_mode(self, strategy_id: int = None):
    #     pass

    @abstractmethod
    async def get_trade_record(
            self,
            acc_id,
            code=None,
            start: datetime = None,
            end: datetime = None,
            strategy_id: int = None,
            limit: int = 1,
    ) -> DataFrame:
        pass

    @abstractmethod
    async def get_position_list(self, acc_id: str, strategy_id: int) -> list[Position]:
        pass

    @abstractmethod
    async def sell(
            self,
            code: str,
            price: float,
            qty: int,
            acc_id: str,
            remark: str = None,
            trade_count: int = None,
            strategy_id: int = None,
    ):
        pass

    @abstractmethod
    async def buy(
            self,
            code: str,
            price: float,
            qty: int,
            acc_id: str,
            remark: str = None,
            trade_count: int = None,
            strategy_id: int = None,
    ):
        pass

    async def update_position_acc_with_new_price(self, code: str, price: float, strategy_id=None):
        pass

    async def update_position_acc_with_kline_df(self, kline_df: DataFrame):
        pass

    async def get_position_count(self, acc_id: str, strategy_id=None):
        pass
