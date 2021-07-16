import pandas as pd
import numpy as np


def period_data(data: pd.DataFrame, period: str) -> pd.DataFrame:
    """
    计算周期指标
    :param data: stock DataFrame
    :param period:
        'W': 以周为周期，每个周期为每周日到周六。
             与'7D'的差别在于'7D'是从当日开始往回计算，不用顾及周的关系。
             值得注意的是，这些周期都是严格按照日期计算的（而不是按照数据行数），就算数据中有日期空缺（周末、节假日）也会计入。
        'D': 以日为周期。
        'M': 以月为周期。
        'Q': 以季为周期。
    :return: 周期性的数据
    """
    data = data.copy()  # 避免在函数内部修改dataframe，影响函数外的数据
    data["date"] = pd.to_datetime(data["date"], format='%Y-%m-%d')
    data.set_index('date', inplace=True)

    period_data = data.resample(period).last()
    period_data['open'] = data['open'].resample(period).first()
    period_data['high'] = data['high'].resample(period).max()
    period_data['low'] = data['low'].resample(period).min()
    period_data['volume'] = data['volume'].resample(period).sum()

    # 股票在有些周一天都没有交易，将这些周去除
    period_data = period_data[period_data['volume'] != 0]
    period_data.reset_index(inplace=True)

    period_data["date"] = period_data["date"].map(lambda x: str(x)[:10])  # 将时间对象转为标准格式的字符串，优化显示效果

    return period_data


def pure_period_data(data: pd.DataFrame, period: str) -> pd.DataFrame:

    if period == 'M':
        period_days = 22
    elif period == 'W':
        period_days = 5
    else:
        raise ValueError("period should be 'M' or 'W'")

    data = data.copy()
    # data["date"] = pd.to_datetime(data["date"])

    period_data = data.iloc[-1::-period_days].reset_index(drop=True)
    period_data['open'] = data['open'].iloc[-period_days:0:-period_days].reset_index(drop=True)
    period_data = period_data[::-1].reset_index(drop=True)
    period_data['high'] = data['high'].groupby(lambda x:x//5).max()
    period_data['low'] = data['low'].groupby(lambda x:x//5).min()
    period_data['volume'] = data['volume'].groupby(lambda x:x//5).sum()
    return period_data


def is_macd_rising(data):
    return data['macd'].iloc[-1] > data['macd'].iloc[-2]


def ene(data):
    pass

# TODO: 智能选取系数
def avg_break_down(data, coef=2):
    data = data.iloc[-22:]
    break_down = data['ma22'] - data['low']
    avg_break_down = break_down[break_down > 0].mean() * coef
    return 0 if np.isnan(avg_break_down) else avg_break_down

