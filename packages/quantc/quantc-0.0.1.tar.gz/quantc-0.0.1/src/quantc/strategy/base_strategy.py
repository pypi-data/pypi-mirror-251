from abc import ABC, abstractmethod
from datetime import datetime
from logging import Logger

import pandas as pd
import talib
from numpy import ndarray

from ..common.data_object import AccInfo, KlineData, Position, TradeRecord
from .db_util import DBUtil
from .quote_gateway import QuoteGateway
from .trade_gateway import TradeGateway
from . import config


class BaseStrategy(ABC):
    STRATEGY_ID = 10000

    # 类级公共变量运行时
    # var_runtime = {}

    # # 类级公共变量持久化
    # var_persistence = {}
    # _db = None

    def __init__(
            self,
            code: str,
            quote: QuoteGateway,
            trade: TradeGateway,
            acc_id: str,
            separate_acc_mode=False,
            dbs: DBUtil = None,
            is_prd_env=False,
    ):
        self.logger: Logger = config.get_logger()
        self.code = code
        self.quote = quote
        self.trade = trade
        self.separate_acc_mode = separate_acc_mode
        self.acc_id = acc_id
        self._is_prd_env = is_prd_env
        # 自动持久化的策略参数
        self.params: dict = None
        self._db: DBUtil = dbs
        self._init_params()

    # 此方法回测环境不调用
    async def init(self):
        # self.parmas = await self.get_parmas()
        await self.init_parmas_from_db()

    # 此方法回测环境不调用
    async def init_parmas_from_db(self):
        self.params = await self.get_params()

    @abstractmethod
    def _init_params(self):
        pass

    def get_code(self) -> str:
        return self.code

    @abstractmethod
    async def on_bar(self, kline_data: KlineData) -> None:
        pass

    # @abstractmethod
    async def on_bar_list(self, kline_list: list[KlineData]) -> list[KlineData]:
        return kline_list

    # 此方法回测环境不调用
    async def on_bar_end(self, kline_data: KlineData) -> None:
        await self.save_params(self.params)

    async def on_position_price_updated(self, kline: KlineData):
        pass

    async def get_cur_day_kline(self, code: str = None, num: int = 181) -> pd.DataFrame:
        """
        获取实时日K线
        :param code: 标的代码
        :param num:K线数量
        :return: DataFrame
        """
        _code = code or self.code
        data = await self.quote.get_cur_day_kline(_code, num)
        return data

    # async def get_cur_day_1m_kline(self) -> DataFrame:
    #     """
    #     获取当天的所有1分钟K线
    #     :return:
    #     """
    #     data = await self.quote.get_cur_day_1m_kline(self.code)
    #     return data

    @staticmethod
    def cla_cur_and_pre_ma(data: ndarray, period=5):
        ma = talib.MA(data[-(period + 1)::], period)[-2::]
        pre_ma = ma[0]
        cur_ma = ma[1]
        return pre_ma, cur_ma

    @staticmethod
    def get_long_ma_flag(data: ndarray, price, period=200):
        ma = talib.MA(data[-(period + 1)::], period)
        return price > ma[-1]

    async def get_params(self) -> dict:
        d = await self._db.get_strategy_params(
            acc_id=self.acc_id, code=self.code, strategy_id=self.STRATEGY_ID
        )
        return d

    async def save_params(self, params: dict):
        await self._db.update_addnew_strategy_params(
            acc_id=self.acc_id, code=self.code, strategy_id=self.STRATEGY_ID, parmas=params
        )

    async def get_position(self) -> Position:
        return await self.trade.get_position(self.code, self.acc_id, self.STRATEGY_ID)

    async def get_acc_info(self) -> AccInfo:
        acc = await self.trade.get_acc_info(self.acc_id)
        return acc

    async def get_position_count(self) -> int:
        count = await self.trade.get_position_count(self.acc_id, self.STRATEGY_ID)
        return count

    async def get_position_list(self) -> list[Position]:
        plist = await self.trade.get_position_list(self.acc_id, self.STRATEGY_ID)
        return plist

    async def get_trade_record(
            self, start: datetime = None, end: datetime = None, limit=5
    ) -> pd.DataFrame:
        trade_record = await self.trade.get_trade_record(
            acc_id=self.acc_id,
            code=self.code,
            strategy_id=self.STRATEGY_ID,
            start=start,
            end=end,
            limit=limit,
        )

        return trade_record

    async def buy(self, price, qty, remark: str = None, trade_count: int = None) -> TradeRecord:
        tr = await self.trade.buy(
            code=self.code,
            price=price,
            qty=qty,
            acc_id=self.acc_id,
            remark=remark,
            trade_count=trade_count,
            strategy_id=self.STRATEGY_ID,
        )
        return tr

    async def sell(self, price, qty, remark: str = None, trade_count: int = None) -> TradeRecord:
        tr = await self.trade.sell(
            code=self.code,
            price=price,
            qty=qty,
            acc_id=self.acc_id,
            remark=remark,
            trade_count=trade_count,
            strategy_id=self.STRATEGY_ID,
        )
        return tr
