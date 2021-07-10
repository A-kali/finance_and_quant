import os
import pytz
from datetime import datetime, timedelta
import talib
import pandas as pd
import datetime
from chinese_calendar import is_workday
import akshare as ak
import warnings
from stock_list import stock_list

save_path = 'akshare_dataframe'


def get_stock(stock_code, data_num):
    # 寻找最后一个已结束的交易日
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    if is_workday(now):
        # 如果是交易日的下午三点之前，则使用前一天的数据
        if now.hour < 15:
            now -= timedelta(days=1)
    while not is_workday(now):
        now -= timedelta(days=1)
    str_date = now.strftime('%Y%m%d')

    if not os.path.exists(f'{save_path}/{stock_code}_{str_date}.csv'):
        data = ak.stock_zh_a_hist(stock_code[:-3], adjust='qfq')
        os.remove(f'{save_path}/{stock_code}*.csv')
        data.to_csv(f'{save_path}/{stock_code}_{str_date}.csv', index=False)
    else:
        data = pd.read_csv(f'{save_path}/{stock_code}_{str_date}.csv', index_col='日期')

    if len(data) > data_num:
        data = data[-data_num:]
    else:
        warnings.warn('Insufficient data')

    return data.reset_index()


def get_indicators(stock_code, data_num):
    data = get_stock(stock_code, data_num)
    data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['收盘'])
    data["ma5"] = talib.EMA(data['收盘'], timeperiod=5)
    data["ma22"] = talib.EMA(data['收盘'], timeperiod=22)
    data["rsi"] = talib.RSI(data['收盘'])
    return data


if __name__ == '__main__':
    for sid, _ in stock_list.items():
        pass
