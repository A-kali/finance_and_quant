import pandas as pd
import pandas_datareader as web
from datetime import datetime, timedelta
import talib
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.ticker as ticker

from stock_list import stock_list

def stock(stock_code): #stock_code是股票代码，例子：上市 "600036.ss", 深市 "000001.sz"
    start_date = "2021-1-01"  #起始日期
    today = datetime.date(datetime.now())  #截止日期
    stock_info = web.get_data_yahoo(stock_code, start_date, today)  #获取行情数据，返回dataframe
    stock_info = stock_info.reset_index()  #默认index是日期，这里要重置一下，为后面绘图做准备
    stock_info = stock_info.astype({"Date": str})    #将Date列的类型设置为str，为绘图做准备
    return stock_info


def get_indicators(stock_code):
    # 创建dataframe
    # data = stock(stock_code)
    data = pd.read_csv('akshare_dataframe/300999_20210709.csv')#[-99:]  # TODO: 加个判断，如果本地有当日文件就访问本地文件，否则同步更新
    # data = data[-100:]

    # 获取macd
    # data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['Close'])
    data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['收盘'])

    data["ma5"] = talib.EMA(data['收盘'], timeperiod=5)
    data["ma22"] = talib.EMA(data['收盘'], timeperiod=22)

    # 获取rsi
    data["rsi"] = talib.RSI(data['收盘'])
    return data


def plot_chart(data, title):
    fig = plt.figure()  # 创建绘图区，包含四个子图
    fig.set_size_inches((10, 8))
    ax_candle = fig.add_axes((0, 0.4, 1, 0.5))  # 蜡烛图子图  # left, bottom, width, height
    ax_macd = fig.add_axes((0, 0, 1, 0.3), sharex=ax_candle)  # macd子图
    # ax_rsi = fig.add_axes((0, 0.24, 1, 0.2), sharex=ax_candle)  # rsi子图
    # ax_vol = fig.add_axes((0, 0, 1, 0.2), sharex=ax_candle)  # 成交量子图

    ohlc = []  # 存放行情数据，candlestick_ohlc需要传入固定格式的数据
    row_number = 0
    for date, row in data.iterrows():
        date, openp, closep, highp, lowp = row[:5]
        ohlc.append([row_number, openp, highp, lowp, closep])
        row_number = row_number + 1

    date_tickers = data['日期'].values  # 获取Date数据

    def format_date(x, pos=None):
        # 由于前面股票数据在 date 这个位置传入的都是int
        # 因此 x=0,1,2,...
        # date_tickers 是所有日期的字符串形式列表
        if x < 0 or x > len(date_tickers) - 1:
            return ''
        return date_tickers[int(x)]

    # 绘制蜡烛图
    ax_candle.plot(data.index, data["ma5"], label="MA5")
    ax_candle.plot(data.index, data["ma22"], label="MA22")
    candlestick_ohlc(ax_candle, ohlc, colorup="g", colordown="r", width=0.8)

    ax_candle.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    ax_candle.xaxis.set_major_locator(ticker.MultipleLocator(20))  # 设置X轴标记、网格间隔
    ax_candle.grid(True)
    ax_candle.set_title(title, fontsize=20)
    ax_candle.legend()

    # 绘制MACD
    ax_macd.plot(data.index, data["macd"], label="macd")
    ax_macd.bar(data.index, data["macd_hist"] * 3, label="hist")
    ax_macd.plot(data.index, data["macd_signal"], label="signal")
    ax_macd.set_title('MACD')
    ax_macd.legend()

    # # 绘制RSI
    # ax_rsi.set_ylabel("(%)")
    # ax_rsi.plot(data.index, [70] * len(data.index), label="overbought")
    # ax_rsi.plot(data.index, [30] * len(data.index), label="oversold")
    # ax_rsi.plot(data.index, data["rsi"], label="rsi")
    # ax_rsi.set_title('KDJ')
    # ax_rsi.legend()

    # 绘制成交量
    # ax_vol.bar(data.index, data["Volume"] / 1000000)
    # ax_vol.set_ylabel("(Million)")

    # fig.savefig("/Users/answer/Desktop/investment/photos/" + title + ".png", bbox_inches="tight")
    plt.show()

def industry(dict):
    # for key, value in dict.items():
    #     d.iteritems: an iterator over the (key, value) items
        # stock_info = get_indicators(key)
        # plot_chart(stock_info, value)
    stock_info = get_indicators(233)
    plot_chart(stock_info, 'lxjm')

if __name__ == '__main__':
    industry(stock_list)
