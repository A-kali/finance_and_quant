import pandas as pd
import numpy as np


def get_period_indicators(period):
    data1="股票日线数据列表"
    stock_data = pd.DataFrame(data1)
    # stock_data.rename(columns={0:'date',1:'open',2:'close',3:'low',4:'high',5:'volume'},inplace=True)

    #设定转换周期period  转换为周是'W',月'M',季度线'Q',五分钟'5min',12天'12D'
    stock_data["date"] = pd.to_datetime(stock_data["date"])
    # period = 'W'
    stock_data.set_index('date',inplace=True)

    #进行转换，周线的每个变量都等于那一周中最后一个交易日的变量
    period_stock_data = stock_data.resample(period).last()
    # 周线的open等于那一周中第一个交易日的open
    period_stock_data['open'] = stock_data['open'].resample(period).first()
    #周线的high等于那一周中的high的最大值
    period_stock_data['high'] = stock_data['high'].resample(period).max()
    #周线的low等于那一周中的low的最大值
    period_stock_data['low'] = stock_data['low'].resample(period).min()
    #周线的volume和money等于那一周中volume和money各自的和
    period_stock_data['volume'] = stock_data['volume'].resample(period).sum()
    # period_stock_data['money'] = stock_data['money'].resample(period,how='sum')
    #计算周线turnover
    # period_stock_data['turnover'] = period_stock_data['volume'](period_stock_data['traded_market_value']/period_stock_data['close'])

    #股票在有些周一天都没有交易，将这些周去除
    period_stock_data = period_stock_data[period_stock_data['volume'].notnull()]
    period_stock_data.reset_index(inplace=True)

    data = np.array(period_stock_data) #先将数据框转换为数组
    data_list = data.tolist()  #其次转换为列表
    for i in data_list:
        i[0]=str(i[0]).split(" ")[0]
    return data_list
