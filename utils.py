import pandas as pd
import numpy as np


def get_period_indicators(data, period):
    data["date"] = pd.to_datetime(data["date"])
    data.set_index('date',inplace=True)

    period_data = data.resample(period).last()
    period_data['open'] = data['open'].resample(period).first()
    period_data['high'] = data['high'].resample(period).max()
    period_data['low'] = data['low'].resample(period).min()
    period_data['volume'] = data['volume'].resample(period).sum()

    #股票在有些周一天都没有交易，将这些周去除
    period_data = period_data[period_data['volume'].notnull()]
    period_data.reset_index(inplace=True)

    data = np.array(period_data) #先将数据框转换为数组
    data_list = data.tolist()  #其次转换为列表
    for i in data_list:
        i[0]=str(i[0]).split(" ")[0]
    return data_list  # TODO: 验证W和7D/5D是不是一样的


def get_period_indicators2(data, period):
    data["date"] = pd.to_datetime(data["date"])
    data.set_index('date',inplace=True)

    period_data = data.resample(period).last()
    period_data['open'] = data['open'].resample(period).first()
    period_data['high'] = data['high'].resample(period).max()
    period_data['low'] = data['low'].resample(period).min()
    period_data['volume'] = data['volume'].resample(period).sum()

    #股票在有些周一天都没有交易，将这些周去除
    period_data = period_data[period_data['volume'].notnull()]
    period_data.reset_index(inplace=True)

    data = np.array(period_data) #先将数据框转换为数组
    data_list = data.tolist()  #其次转换为列表
    for i in data_list:
        i[0]=str(i[0]).split(" ")[0]
    return data_list
