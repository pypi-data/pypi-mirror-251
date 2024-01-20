import time
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from .constant import Market


def get_datetime_now(market: Market = Market.HK):
    if market == Market.US:
        # 创建时区对象
        eastern = ZoneInfo('US/Eastern')

        # 创建本地日期时间对象
        local_dt = datetime.now(eastern)
        return local_dt
    else:
        return datetime.now()


def gen_uuid():
    return uuid.uuid4().hex


def get_exchange(market: str) -> str:
    if market == "HK":
        return "HKE"
    else:
        return "SSE"


def today() -> str:
    return time.strftime("%Y-%m-%d", time.localtime())


def parse_time(date_str: str, time_str: str):
    return time.mktime(time.strptime('%s %s'.format(date_str, time_str), "%Y-%m-%d %H:%M"))


if __name__ == '__main__':
    print(get_datetime_now(Market.US))
