import pandas as pd
import datetime

from xtquant import xtdatacenter as xtdc, xtdata
from xtquant.xtdata import (
    get_local_data,
    download_history_data,
)

from mason_tools import RpcServer


def init_xt(xt_token: str):
    xtdc.set_token(xt_token)
    xtdc.init()


def get_history_data(stock_code, period, start_time="", end_time=""):
    download_history_data(
        stock_code, period, start_time=start_time, end_time=end_time, incrementally=None
    )
    data: dict = get_local_data(
        [], [stock_code], period, start_time, end_time, -1, "front_ratio", False
    )  # 默认等比前复权

    df: pd.DataFrame = data[stock_code]
    df["time"] = df["time"].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000))
    df["stock_code"] = stock_code

    return df


def xt_data(func_name, *args, **kwargs):
    return getattr(xtdata, func_name)(*args, **kwargs)


def test_xt(
    xt_token,
    start_date="20240110",
    end_date="20240112",
    period="1m",
    symbol="rb2405.SF",
):
    init_xt(xt_token)
    return get_history_data(symbol, period, start_date, end_date)


def XtDataServer(xt_token, rep_address, pub_address):
    init_xt(xt_token)
    xt_server = RpcServer()
    xt_server.start(rep_address, pub_address)
    xt_server.register(xt_data)
    xt_server.register(get_history_data)
    return xt_server


if __name__ == "__main__":
    xt_token = ""
    rep_address = "tcp://*:2014"
    pub_address = "tcp://*:4102"
    # test_xt(xt_token)
    s = XtDataServer(xt_token, rep_address, pub_address)
