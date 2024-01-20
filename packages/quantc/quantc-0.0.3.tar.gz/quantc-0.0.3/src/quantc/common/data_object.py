from dataclasses import dataclass, field
from datetime import datetime, date

import msgpack
import pandas as pd
from quantc.common.constant import (
    TIME_KEY_FORMAT,
    Currency,
    Exchange,
    KLType,
    PositionSide,
)
from quantc.common.util import gen_uuid


@dataclass
class BaseData:
    """
    Any data object needs a gateway_name as source
    and should inherit base data.
    """

    gateway_name: str = None


@dataclass
class KlineData(BaseData):
    """
    Candlestick bar data of a certain trading period.
    """

    gateway_name: str = None
    code: str = None
    time_key: str = None

    k_type: KLType = None
    volume: float = 0
    turnover: float = 0
    open: float = 0
    high: float = 0
    low: float = 0
    close: float = 0
    pe_ratio: float = 0
    turnover_rate: float = 0
    last_close: float = 0
    # 某些指数的k线会有均价
    avg_price: float = 0
    lot_size: int = 100
    date_time: datetime = None

    # 期货相关属性
    # 结算价 （仅限日线数据）
    settlement: float = 0
    # 昨日结算价（仅限日线数据）
    prev_settlement: float = 0
    # 累计持仓量
    open_interest: float = 0

    # 当前合约的持仓量

    def to_dataframe(self):
        di = self.__dict__
        # del di['date_time']
        # del di['gateway_name']
        # print(di)
        return pd.DataFrame([di])

    def __post_init__(self) -> None:
        self.date_time: datetime = datetime.fromisoformat(self.time_key)


# @dataclass
# class Position:
#     """
#     持仓信息
#     """

#     code: str
#     name: str = None
#     # 持有数量
#     qty: float = None
#     # 可卖数量
#     can_sell_qty: float = None
#     # 市价
#     nominal_price: float = None
#     # 摊薄成本价（证券账户），平均开仓价（期货账户）
#     cost_price: float = None
#     # 市值
#     market_val: float = None

#     create_time: datetime = None
#     strategy_id: int = None
#     # order_status: str = None
#     position_side: PositionSide = None  ************************
#     pnl: float = 0
#     maintenance_margin: float = 0


@dataclass
class Position:
    """
    持仓信息
    """

    acc_id: str
    code: str
    ps_id: str = field(default_factory=gen_uuid)
    name: str = None
    # 持有数量
    qty: float = None
    # 可卖数量
    can_sell_qty: float = None
    # 市价
    nominal_price: float = None
    # 摊薄成本价（证券账户），平均开仓价（期货账户）
    cost_price: float = None
    # 市值
    market_val: float = None

    create_time: str = datetime.now().strftime(TIME_KEY_FORMAT)
    update_time: str = None
    strategy_id: int = None
    position_side: str = PositionSide.LONG.value
    pnl: float = 0
    maintenance_margin: float = 0
    # 最后买卖时间
    last_bs_time: str = datetime.now().strftime(TIME_KEY_FORMAT)

    def __post_init__(self):
        if isinstance(self.update_time, datetime):
            self.update_time = self.update_time.strftime(TIME_KEY_FORMAT)
        if isinstance(self.create_time, datetime):
            self.create_time = self.create_time.strftime(TIME_KEY_FORMAT)


@dataclass
class AccInfo:
    """
    账户信息
    """

    acc_id: str
    # 现金
    cash: float = 0
    # 证券市值
    market_val: float = 0
    # 资产净值
    total_assets: float = None

    # 最大购买力（保证金账户）
    power: float = 0
    # # 卖空购买力
    max_power_short: float = 0
    # # 现金购买力
    net_cash_power: float = 0

    # # 多头市值
    long_mv: float = 0
    # # 空头市值
    short_mv: float = 0

    init_cash: float = None
    update_time: str = datetime.now().isoformat()
    maintenance_margin: float = 0
    frozen_cash: float = 0

    def __post_init__(self):
        if self.total_assets is None:
            self.total_assets = self.cash + self.market_val
        if self.init_cash is None:
            self.init_cash = self.cash
        if self.net_cash_power == 0:
            self.net_cash_power = self.cash - self.frozen_cash
        if not isinstance(self.update_time, str) and self.update_time is not None:
            self.update_time = self.update_time.isoformat()


@dataclass
class OrderRemark:
    counter: int = 0
    remark: str = None


@dataclass
class TradeRecordDb:
    acc_id: str
    order_id: str
    code: str
    stock_name: str

    order_type: str
    order_status: str
    qty: int
    price: float
    create_time: str = datetime.now().isoformat()
    update_time: str = None
    # 成交数量
    dealt_qty: int = None
    # 成交均价
    dealt_avg_price: float = None

    last_err_msg: str = None
    remark: str = None
    strategy_id: int = None
    trd_side: str = None
    updated_dealt_qty: int = 0
    updated_dealt_price: float = 0
    trade_count: float = None
    tr_id: str = None
    tr_remark: str = None

    def __post_init__(self):
        if not isinstance(self.update_time, str) and self.update_time is not None:
            self.update_time = self.update_time.isoformat()
        if not isinstance(self.create_time, str) and self.create_time is not None:
            self.create_time = self.create_time.isoformat()


translation_table = {
    0: (
        AccInfo,
        lambda value: msgpack.packb(
            (
                value.acc_id,
                value.cash,
                value.market_val,
                value.total_assets,
                value.power,
                value.max_power_short,
                value.net_cash_power,
                value.long_mv,
                value.short_mv,
                value.init_cash,
                value.update_time,
                value.maintenance_margin,
                value.frozen_cash,
            )
        ),
        lambda binary: AccInfo(*msgpack.unpackb(binary)),
    ),
    1: (
        Position,
        lambda value: msgpack.packb(
            (
                value.acc_id,
                value.code,
                value.ps_id,
                value.name,
                value.qty,
                value.can_sell_qty,
                value.nominal_price,
                value.cost_price,
                value.market_val,
                value.create_time,
                value.update_time,
                value.strategy_id,
                value.position_side,
                value.pnl,
                value.maintenance_margin,
                value.last_bs_time,
            )
        ),
        lambda binary: Position(*msgpack.unpackb(binary)),
    ),
    2: (
        TradeRecordDb,
        lambda value: msgpack.packb(
            (
                value.acc_id,
                value.order_id,
                value.code,
                value.stock_name,
                value.order_type,
                value.order_status,
                value.qty,
                value.price,
                value.create_time,
                value.update_time,
                value.dealt_qty,
                value.dealt_avg_price,
                value.last_err_msg,
                value.remark,
                value.strategy_id,
                value.trd_side,
                value.updated_dealt_qty,
                value.updated_dealt_price,
                value.trade_count,
                value.tr_id,
                value.tr_remark,
            )
        ),
        lambda binary: TradeRecordDb(*msgpack.unpackb(binary)),
    ),
}


@dataclass
class TradeRecord(TradeRecordDb):
    date: date = None
    amount: float = None
    pnl: float = None
    cost_price: float = None
    total_assets: float = None


@dataclass
class Contract:
    """
    ``Contract(**kwargs)`` can create any contract using keyword
    arguments. To simplify working with contracts, there are also more
    specialized contracts that take optional positional arguments.
    Some examples::

        Contract(conId=270639)
        Stock('AMD', 'SMART', 'USD')
        Stock('INTC', 'SMART', 'USD', primaryExchange='NASDAQ')
        Forex('EURUSD')
        CFD('IBUS30')
        Future('ES', '20180921', 'GLOBEX')
        Option('SPY', '20170721', 240, 'C', 'SMART')
        Bond(secIdType='ISIN', secId='US03076KAA60')
        Crypto('BTC', 'PAXOS', 'USD')

    Args:
        conId (int): The unique IB contract identifier.
        code (str): The contract (or its underlying) code.
        secType (str): The security type:

            * 'STK' = Stock (or ETF)
            * 'OPT' = Option
            * 'FUT' = Future
            * 'IND' = Index
            * 'FOP' = Futures option
            * 'CASH' = Forex pair
            * 'CFD' = CFD
            * 'BAG' = Combo
            * 'WAR' = Warrant
            * 'BOND' = Bond
            * 'CMDTY' = Commodity
            * 'NEWS' = News
            * 'FUND' = Mutual fund
            * 'CRYPTO' = Crypto currency
        lastTradeDateOrContractMonth (str): The contract's last trading
            day or contract month (for Options and Futures).
            Strings with format YYYYMM will be interpreted as the
            Contract Month whereas YYYYMMDD will be interpreted as
            Last Trading Day.
        strike (float): The option's strike price.
        right (str): Put or Call.
            Valid values are 'P', 'PUT', 'C', 'CALL', or '' for non-options.
        multiplier (str): he instrument's multiplier (i.e. options, futures).
        exchange (str): The destination exchange.
        currency (str): The underlying's currency.
        localcode (str): The contract's code within its primary exchange.
            For options, this will be the OCC code.
        primaryExchange (str): The contract's primary exchange.
            For smart routed contracts, used to define contract in case
            of ambiguity. Should be defined as native exchange of contract,
            e.g. ISLAND for MSFT. For exchanges which contain a period in name,
            will only be part of exchange name prior to period, i.e. ENEXT
            for ENEXT.BE.
        tradingClass (str): The trading class name for this contract.
            Available in TWS contract description window as well.
            For example, GBL Dec '13 future's trading class is "FGBL".
        includeExpired (bool): If set to true, contract details requests
            and historical data queries can be performed pertaining to
            expired futures contracts. Expired options or other instrument
            types are not available.
        secIdType (str): Security identifier type. Examples for Apple:

                * secIdType='ISIN', secId='US0378331005'
                * secIdType='CUSIP', secId='037833100'
        secId (str): Security identifier.
        comboLegsDescription (str): Description of the combo legs.
        comboLegs (List[ComboLeg]): The legs of a combined contract definition.
        deltaNeutralContract (DeltaNeutralContract): Delta and underlying
            price for Delta-Neutral combo orders.
    """

    secType: str = ''
    # conId: int = 0
    code: str = ''
    lastTradeDateOrContractMonth: str = ''
    strike: float = 0.0
    right: str = ''
    multiplier: str = ''
    exchange: Exchange = None
    primaryExchange: str = ''
    currency: Currency = None
    # localcode: str = ''
    # tradingClass: str = ''
    includeExpired: bool = False

    # secIdType: str = ''
    # secId: str = ''
    # comboLegsDescrip: str = ''
    # comboLegs: List['ComboLeg'] = field(default_factory=list)
    # deltaNeutralContract: Optional['DeltaNeutralContract'] = None

    @staticmethod
    def create(**kwargs) -> 'Contract':
        """
        Create and a return a specialized contract based on the given secType,
        or a general Contract if secType is not given.
        """
        secType = kwargs.get('secType', '')
        cls = {
            '': Contract,
            'STK': Stock,
            'OPT': Option,
            'FUT': Future,
            # 'CONTFUT': ContFuture,
            # 'CASH': Forex,
            # 'IND': Index,
            # 'CFD': CFD,
            # 'BOND': Bond,
            # 'CMDTY': Commodity,
            # 'FOP': FuturesOption,
            # 'FUND': MutualFund,
            # 'WAR': Warrant,
            # 'IOPT': Warrant,
            # 'BAG': Bag,
            # 'CRYPTO': Crypto,
            # 'NEWS': Contract
        }.get(secType, Contract)
        if cls is not Contract:
            kwargs.pop('secType', '')
        return cls(**kwargs)


class Stock(Contract):
    def __init__(
            self, code: str = '', exchange: Exchange = None, currency: Currency = None, **kwargs
    ):
        """
        Stock contract.

        Args:
            code: code name.
            exchange: Destination exchange.
            currency: Underlying currency.
        """
        Contract.__init__(
            self, secType='STK', code=code, exchange=exchange, currency=currency, **kwargs
        )


class Option(Contract):
    def __init__(
            self,
            code: str = '',
            lastTradeDateOrContractMonth: str = '',
            strike: float = 0.0,
            right: str = '',
            exchange: Exchange = None,
            multiplier: str = '',
            currency: Currency = None,
            **kwargs,
    ):
        """
        Option contract.

        Args:
            code: code name.
            lastTradeDateOrContractMonth: The option's last trading day
                or contract month.

                * YYYYMM format: To specify last month
                * YYYYMMDD format: To specify last trading day
            strike: The option's strike price.
            right: Put or call option.
                Valid values are 'P', 'PUT', 'C' or 'CALL'.
            exchange: Destination exchange.
            multiplier: The contract multiplier.
            currency: Underlying currency.
        """
        Contract.__init__(
            self,
            'OPT',
            code=code,
            lastTradeDateOrContractMonth=lastTradeDateOrContractMonth,
            strike=strike,
            right=right,
            exchange=exchange,
            multiplier=multiplier,
            currency=currency,
            **kwargs,
        )


class Future(Contract):
    def __init__(
            self,
            code: str = '',
            lastTradeDateOrContractMonth: str = '',
            exchange: Exchange = None,
            # localcode: str = '',
            multiplier: str = '',
            currency: Currency = None,
            **kwargs,
    ):
        """
        Future contract.

        Args:
            code: code name.
            lastTradeDateOrContractMonth: The option's last trading day
                or contract month.

                * YYYYMM format: To specify last month
                * YYYYMMDD format: To specify last trading day
            exchange: Destination exchange.
            localcode: The contract's code within its primary exchange.
            multiplier: The contract multiplier.
            currency: Underlying currency.
        """
        Contract.__init__(
            self,
            'FUT',
            code=code,
            lastTradeDateOrContractMonth=lastTradeDateOrContractMonth,
            exchange=exchange,
            # localcode=localcode,
            multiplier=multiplier,
            currency=currency,
            **kwargs,
        )


@dataclass
class OrderBookData:
    price: float
    volume: int
    order_num: int


@dataclass
class OrderBook:
    ask: list[OrderBookData]
    bid: list[OrderBookData]
