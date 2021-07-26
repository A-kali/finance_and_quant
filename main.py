import os
import glob
import talib
import pandas as pd
import akshare as ak
import warnings

from visualize import plot_chart
from utils import period_data, pure_period_data, latest_trading_day
from pool import english_columns, StockPool
from strategy import TripleScreen

save_path = 'akshare_dataframe'


def get_stock(stock_code, data_num) -> pd.DataFrame:
    str_date = latest_trading_day()
    if not os.path.exists(f'{save_path}/{stock_code}_{str_date}.csv'):
        data = ak.stock_zh_a_hist(stock_code, adjust='qfq')
        data.rename(columns=english_columns, inplace=True)
        for f in glob.glob(f'{save_path}/{stock_code}*.csv'):
            os.remove(f)
            print(f'update: {stock_code}_{str_date}.csv')
        data.to_csv(f'{save_path}/{stock_code}_{str_date}.csv', index=False)
    else:
        data = pd.read_csv(f'{save_path}/{stock_code}_{str_date}.csv')

    if len(data) > data_num:
        data = data[-data_num:]
    else:
        warnings.warn('Insufficient data')

    return data.reset_index(drop=True)


def get_base_indicators(data):
    data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['close'])
    data["ma5"] = talib.EMA(data['close'], timeperiod=5)
    data["ma22"] = talib.EMA(data['close'], timeperiod=22)
    data["rsi"] = talib.RSI(data['close'])
    return data


if __name__ == '__main__':
    sp = StockPool()
    # sp.add('000516')
    for i, row in sp:
        data = get_stock(row['code'][:6], 200)  # 至少需要180天以上（26×7+假期）
        data_week = pure_period_data(data, 'W')
        data = get_base_indicators(data)
        # plot_chart(data_week1, sid)

        print(row['code'], row['name'], row['price'], end=None)
        ts = TripleScreen(data, row['price'], 240000)
        ts.choose()


# TODO: 计算ENE
# TODO: 智能选取ENE参数

# TODO: 回溯
# TODO: 爬虫
# TODO: 交互界面
