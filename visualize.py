import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mplfinance.original_flavor import candlestick_ohlc

def plot_chart(data, title):
    fig = plt.figure()  # 创建绘图区，包含四个子图
    fig.set_size_inches((20, 16))
    ax_candle = fig.add_axes((0, 0.72, 1, 0.32))  # 蜡烛图子图
    ax_macd = fig.add_axes((0, 0.48, 1, 0.2), sharex=ax_candle)  # macd子图
    ax_rsi = fig.add_axes((0, 0.24, 1, 0.2), sharex=ax_candle)  # rsi子图
    ax_vol = fig.add_axes((0, 0, 1, 0.2), sharex=ax_candle)  # 成交量子图

    ohlc = []  # 存放行情数据，candlestick_ohlc需要传入固定格式的数据
    row_number = 0
    for date, row in data.iterrows():
        date, highp, lowp, openp, closep = row[:5]
        ohlc.append([row_number, openp, highp, lowp, closep])
        row_number = row_number + 1

    date_tickers = data.Date.values  # 获取Date数据

    def format_date(x, pos=None):
        # 由于前面股票数据在 date 这个位置传入的都是int
        # 因此 x=0,1,2,...
        # date_tickers 是所有日期的字符串形式列表
        if x < 0 or x > len(date_tickers) - 1:
            return ''
        return date_tickers[int(x)]

    # 绘制蜡烛图
    ax_candle.plot(data.index, data["ma7"], label="MA7")
    ax_candle.plot(data.index, data["ma8"], label="MA8")
    ax_candle.plot(data.index, data["ma25"], label="MA25")
    candlestick_ohlc(ax_candle, ohlc, colorup="g", colordown="r", width=0.8)

    ax_candle.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    ax_candle.xaxis.set_major_locator(ticker.MultipleLocator(6))  # 设置间隔为6个交易日
    ax_candle.grid(True)
    ax_candle.set_title(title, fontsize=20)
    ax_candle.legend()

    # 绘制MACD
    ax_macd.plot(data.index, data["macd"], label="macd")
    ax_macd.bar(data.index, data["macd_hist"] * 3, label="hist")
    ax_macd.plot(data.index, data["macd_signal"], label="signal")
    ax_macd.set_title('MACD')
    ax_macd.legend()

    # 绘制RSI
    ax_rsi.set_ylabel("(%)")
    ax_rsi.plot(data.index, [70] * len(data.index), label="overbought")
    ax_rsi.plot(data.index, [30] * len(data.index), label="oversold")
    ax_rsi.plot(data.index, data["rsi"], label="rsi")
    ax_rsi.set_title('KDJ')
    ax_rsi.legend()

    # 绘制成交量
    ax_vol.bar(data.index, data["Volume"] / 1000000)
    ax_vol.set_ylabel("(Million)")

    # fig.savefig("/Users/answer/Desktop/investment/photos/" + title + ".png", bbox_inches="tight")
    plt.show()

