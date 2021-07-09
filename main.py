import akshare as ak
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

from stock_list import stock_list

df_path = 'akshare_dataframe'

def expma(N, arr):
    arr = arr[:N]
    x = arr[0]
    for a in arr[1:]:
        x = ((2 * a) + (N - 1) * x) / (N + 1)
    return x

def macd(arr):
    return (224 / 51 * expma(9, arr))\
           - (16 / 3 * expma(12, arr))\
           + (16 / 17 * expma(26, arr))

if __name__ == '__main__':
    for _, sid in stock_list.items():
        df = ak.stock_zh_a_hist('002475', adjust='qfq')
        df.to_csv(f"{df_path}/{sid}_{str(datetime.date.today()).replace('-', '')}.csv", index=False)

    # df = pd.read_csv('002475_20210709.csv')['收盘']
    # day_closing_prices = np.array(df)[::-1]
    # week_closing_prices = np.array(df)[::-5]
    # week_macd = [macd(week_closing_prices[i:]) for i in range(19, -1, -1)]
    #
    # bar_plot = sns.relplot(x=range(20), y=week_macd, kind='line')
    # plt.xticks(rotation=90)
    # plt.show()
