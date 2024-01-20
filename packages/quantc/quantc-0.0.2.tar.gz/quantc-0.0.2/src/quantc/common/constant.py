from enum import Enum

KLINE_DAY_TABLE_NAME = '_DAY_KLINE'
KLINE_1M_TABLE_NAME = '_1M_KLINE'

RET_OK = 0
RET_ERROR = -1

TIME_KEY_FORMAT = '%Y-%m-%d %H:%M:%S'


class GlobalIndex(str, Enum):
    # USI = 'USDindex'
    USI = 'IDX.USI'
    HSI = 'HK.800000'
    SPY = 'US.SPY'


class Market(str, Enum):
    """
    标识不同的行情市场，股票名称的前缀复用该字符串,如 **'HK.00700'**, **'HK_FUTURE.999010'**
    ..  py:class:: Market
     ..  py:attribute:: HK
      港股
     ..  py:attribute:: US
      美股
     ..  py:attribute:: SH
      沪市
     ..  py:attribute:: SZ
      深市
     ..  py:attribute:: HK_FUTURE
      港股期货
     ..  py:attribute:: NONE
      未知
    """

    NONE = "N/A"
    HK = "HK"
    US = "US"
    SH = "SH"
    SZ = "SZ"
    HK_FUTURE = "HK_FUTURE"
    SG = "SG"
    JP = "JP"
    CH_FUTURE = "CH_FUTURE"


class KLType(str, Enum):
    """
    k线类型定义
    ..  py:class:: KLType
     ..  py:attribute:: K_1M
      1分钟K线
     ..  py:attribute:: K_5M
      5分钟K线
     ..  py:attribute:: K_15M
      15分钟K线
     ..  py:attribute:: K_30M
      30分钟K线
     ..  py:attribute:: K_60M
      60分钟K线
     ..  py:attribute:: K_DAY
      日K线
     ..  py:attribute:: K_WEEK
      周K线
     ..  py:attribute:: K_MON
      月K线
    """

    NONE = "N/A"
    K_1M = "K_1M"
    K_3M = "K_3M"
    K_5M = "K_5M"
    K_15M = "K_15M"
    K_30M = "K_30M"
    K_60M = "K_60M"
    K_DAY = "K_DAY"
    K_WEEK = "K_WEEK"
    K_MON = "K_MON"
    K_QUARTER = "K_QUARTER"
    K_YEAR = "K_YEAR"


class TrdSide(str, Enum):
    """
    交易方向类型定义(客户端下单只传Buy或Sell即可，SELL_SHORT / BUY_BACK 服务器可能会传回)
    ..  py:class:: TrdSide
     ..  py:attribute:: NONE
      未知
    ..  py:attribute:: BUY
      买
     ..  py:attribute:: SELL
      卖
     ..  py:attribute:: SELL_SHORT
      卖空
     ..  py:attribute:: BUY_BACK
      买回
    """

    NONE = "N/A"
    BUY = "BUY"
    SELL = "SELL"
    SELL_SHORT = "SELL_SHORT"
    BUY_BACK = "BUY_BACK"


# 持仓方向
class PositionSide(str, Enum):
    """
    持仓方向类型定义
    ..  py:class:: PositionSide
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: LONG
      多仓
     ..  py:attribute:: SHORT
      空仓
    """

    NONE = "N/A"
    LONG = "LONG"  # 多仓
    SHORT = "SHORT"  # 空仓


# class Status(Enum):
#     """
#     Order status.
#     """
#     SUBMITTING = "提交中"
#     NOT_TRADED = "未成交"
#     PART_TRADED = "部分成交"
#     ALL_TRADED = "全部成交"
#     CANCELLED = "已撤销"
#     REJECTED = "拒单"


class OrderType(str, Enum):
    """
    订单类型定义
    ..  py:class:: OrderType
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: NORMAL
      普通订单(港股的增强限价单、A股限价委托、美股的限价单)
     ..  py:attribute:: MARKET
      市价，目前仅美股
     ..  py:attribute:: ABSOLUTE_LIMIT
      港股限价单(只有价格完全匹配才成交)
     ..  py:attribute:: AUCTION
      港股竞价单
     ..  py:attribute:: AUCTION_LIMIT
      港股竞价限价单
     ..  py:attribute:: SPECIAL_LIMIT
      港股特别限价(即市价IOC, 订单到达交易所后，或全部成交， 或部分成交再撤单， 或下单失败)
    """

    NONE = "N/A"
    NORMAL = "NORMAL"  # 普通订单(港股的增强限价单、A股限价委托、美股的限价单)
    MARKET = "MARKET"  # 市价，目前仅美股
    ABSOLUTE_LIMIT = "ABSOLUTE_LIMIT"  # 港股_限价(只有价格完全匹配才成交)
    AUCTION = "AUCTION"  # 港股_竞价
    AUCTION_LIMIT = "AUCTION_LIMIT"  # 港股_竞价限价
    # 港股_特别限价(即市价IOC, 订单到达交易所后，或全部成交， 或部分成交再撤单， 或下单失败)
    SPECIAL_LIMIT = "SPECIAL_LIMIT"
    SPECIAL_LIMIT_ALL = "SPECIAL_LIMIT_ALL"  # 港股_特别限价(要么全部成交，要么自动撤单)
    STOP = "STOP"  # 止损市价单
    STOP_LIMIT = "STOP_LIMIT"  # 止损限价单
    MARKET_IF_TOUCHED = "MARKET_IF_TOUCHED"  # 触及市价单（止盈）
    LIMIT_IF_TOUCHED = "LIMIT_IF_TOUCHED"  # 触及限价单（止盈）
    TRAILING_STOP = "TRAILING_STOP"  # 跟踪止损市价单
    TRAILING_STOP_LIMIT = "TRAILING_STOP_LIMIT"  # 跟踪止损限价单


# 订单状态
class OrderStatus(str, Enum):
    """
    订单状态定义
    ..  py:class:: OrderStatus
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: UNSUBMITTED
      未提交
     ..  py:attribute:: WAITING_SUBMIT
      等待提交
     ..  py:attribute:: SUBMITTING
      提交中
     ..  py:attribute:: SUBMIT_FAILED
      提交失败，下单失败
     ..  py:attribute:: SUBMITTED
      已提交，等待成交
     ..  py:attribute:: FILLED_PART
      部分成交
     ..  py:attribute:: FILLED_ALL
      全部已成
     ..  py:attribute:: CANCELLING_PART
      正在撤单部分(部分已成交，正在撤销剩余部分)
     ..  py:attribute:: CANCELLING_ALL
      正在撤单全部
     ..  py:attribute:: CANCELLED_PART
      部分成交，剩余部分已撤单
     ..  py:attribute:: CANCELLED_ALL
      全部已撤单，无成交
     ..  py:attribute:: FAILED
      下单失败，服务拒绝
     ..  py:attribute:: DISABLED
      已失效
     ..  py:attribute:: DELETED
      已删除(无成交的订单才能删除)
    """

    NONE = "N/A"  # 未知状态
    UNSUBMITTED = "UNSUBMITTED"  # 未提交
    WAITING_SUBMIT = "WAITING_SUBMIT"  # 等待提交
    SUBMITTING = "SUBMITTING"  # 提交中
    SUBMIT_FAILED = "SUBMIT_FAILED"  # 提交失败，下单失败
    TIMEOUT = "TIMEOUT"  # 处理超时，结果未知
    SUBMITTED = "SUBMITTED"  # 已提交，等待成交
    FILLED_PART = "FILLED_PART"  # 部分成交
    FILLED_ALL = "FILLED_ALL"  # 全部已成
    CANCELLING_PART = "CANCELLING_PART"  # 正在撤单_部分(部分已成交，正在撤销剩余部分)
    CANCELLING_ALL = "CANCELLING_ALL"  # 正在撤单_全部
    CANCELLED_PART = "CANCELLED_PART"  # 部分成交，剩余部分已撤单
    CANCELLED_ALL = "CANCELLED_ALL"  # 全部已撤单，无成交
    FAILED = "FAILED"  # 下单失败，服务拒绝
    DISABLED = "DISABLED"  # 已失效
    DELETED = "DELETED"  # 已删除，无成交的订单才能删除
    FILL_CANCELLED = "FILL_CANCELLED"  # 成交被撤销，一般遇不到，意思是已经成交的订单被回滚撤销，成交无效变为废单


class Currency(str, Enum):
    """
    Currency.
    """

    USD = "USD"
    HKD = "HKD"
    CNY = "CNY"
    CAD = "CAD"


class Exchange(Enum):
    """
    Exchange.
    """

    # Chinese
    CFFEX = "CFFEX"  # China Financial Futures Exchange
    SHFE = "SHFE"  # Shanghai Futures Exchange
    CZCE = "CZCE"  # Zhengzhou Commodity Exchange
    DCE = "DCE"  # Dalian Commodity Exchange
    INE = "INE"  # Shanghai International Energy Exchange
    GFEX = "GFEX"  # Guangzhou Futures Exchange
    SSE = "SSE"  # Shanghai Stock Exchange
    SZSE = "SZSE"  # Shenzhen Stock Exchange
    BSE = "BSE"  # Beijing Stock Exchange
    SGE = "SGE"  # Shanghai Gold Exchange
    WXE = "WXE"  # Wuxi Steel Exchange
    CFETS = "CFETS"  # CFETS Bond Market Maker Trading System
    XBOND = "XBOND"  # CFETS X-Bond Anonymous Trading System

    # Global
    SMART = "SMART"  # Smart Router for US stocks
    NYSE = "NYSE"  # New York Stock Exchnage
    NASDAQ = "NASDAQ"  # Nasdaq Exchange
    ARCA = "ARCA"  # ARCA Exchange
    EDGEA = "EDGEA"  # Direct Edge Exchange
    ISLAND = "ISLAND"  # Nasdaq Island ECN
    BATS = "BATS"  # Bats Global Markets
    IEX = "IEX"  # The Investors Exchange
    AMEX = "AMEX"  # American Stock Exchange
    TSE = "TSE"  # Toronto Stock Exchange
    NYMEX = "NYMEX"  # New York Mercantile Exchange
    COMEX = "COMEX"  # COMEX of CME
    GLOBEX = "GLOBEX"  # Globex of CME
    IDEALPRO = "IDEALPRO"  # Forex ECN of Interactive Brokers
    CME = "CME"  # Chicago Mercantile Exchange
    ICE = "ICE"  # Intercontinental Exchange
    SEHK = "SEHK"  # Stock Exchange of Hong Kong
    HKFE = "HKFE"  # Hong Kong Futures Exchange
    SGX = "SGX"  # Singapore Global Exchange
    CBOT = "CBT"  # Chicago Board of Trade
    CBOE = "CBOE"  # Chicago Board Options Exchange
    CFE = "CFE"  # CBOE Futures Exchange
    DME = "DME"  # Dubai Mercantile Exchange
    EUREX = "EUX"  # Eurex Exchange
    APEX = "APEX"  # Asia Pacific Exchange
    LME = "LME"  # London Metal Exchange
    BMD = "BMD"  # Bursa Malaysia Derivatives
    TOCOM = "TOCOM"  # Tokyo Commodity Exchange
    EUNX = "EUNX"  # Euronext Exchange
    KRX = "KRX"  # Korean Exchange
    OTC = "OTC"  # OTC Product (Forex/CFD/Pink Sheet Equity)
    IBKRATS = "IBKRATS"  # Paper Trading Exchange of IB

    # Special Function
    LOCAL = "LOCAL"  # For local generated data
