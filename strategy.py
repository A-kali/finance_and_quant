import pandas as pd
from utils import pure_period_data, ene
import talib


class TripleScreen:
    """
    书名：Come Into My Trading RoomA Complete Guide to Trading
    中文名：《走进我的交易室》
    三重滤网交易法
    """
    def __init__(self, data: pd.DataFrame, current_price):
        self.data = data
        self.data_w = pure_period_data(data, 'W')
        self.current_price = current_price

    def _first_screen(self) -> bool:
        """
        判断半年EMA趋势和周MACD趋势是否向上
        :return: bool
        """
        ema_22w = talib.EMA(self.data_w['close'], timeperiod=26)
        macd_w = talib.MACD(self.data_w['close'])[0]
        return ema_22w.iloc[-1] > ema_22w.iloc[-2] and macd_w.iloc[-1] > macd_w.iloc[-2]

    def _second_screen(self, active=False):
        if active:
            pass
        else:
            pass

    def _third_screen(self, active):
        if active:
            pass  # 均线  TODO: 几日均线？
        else:
            pass  # 前一日高点/低点

    def choose(self):
        pass
