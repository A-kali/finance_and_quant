import numpy as np
import pandas as pd
from utils import pure_period_data, ene, avg_break_down, strength_ind
import talib


class TripleScreen:
    """
    书名：Come Into My Trading RoomA Complete Guide to Trading
    中文名：《走进我的交易室》
    三重滤网交易法
    """
    def __init__(self, data: pd.DataFrame, current_price, total_net_worth):
        self.data = data
        self.data_w = pure_period_data(data, 'W')
        self.current_price = current_price if current_price else data['close'].iloc[-1]
        self.total_net_worth = total_net_worth

    def _first_screen(self) -> int:
        """
        判断半年EMA趋势和周MACD趋势是否向上
        """
        mark = 0
        ema_26w = talib.EMA(self.data_w['close'], timeperiod=26)
        if ema_26w.iloc[-1] > ema_26w.iloc[-2]:
            mark += 1
            macd_w = talib.MACD(self.data_w['close'])[0]
            if macd_w.iloc[-1] > macd_w.iloc[-2]:  # 强势向上
                mark += 1
            elif macd_w.iloc[-2] > macd_w.iloc[-3]:  # 顶背离
                mark -= 2
            else:                                   # 弱势向上
                mark -= 1
        else:                                       # 向下
            mark -= 1
        return mark

    def _second_screen(self, active=False):  # TODO: 判断active
        """
        策略A：
        日MACD跌到0以后上扬、或随机指标跌到参考线下
        力度指数的2日EMA到0以下
        只要周趋势向上且触发以上条件就加仓，周趋势反转则获利了结
        策略B：
        使用ENE，触及到上轨就减仓、清仓，触及到均线就加仓、建仓。周趋势反转则获利了结
        """
        if active:
            strength =  strength_ind(self.data)
            if talib.EMA(strength, timeperiod=2)[-1] < 0:
                return True
        else:
            macd = talib.MACD(self.data['close'])[0]  # TODO: MACD应该使用当日的还是前一日的？
            if macd.iloc[-2] <= 0 and macd.iloc[-1] > 0:
                return True
        return False

    def _third_screen(self, active=False, timeperiod=5) -> float:
        """
        判断进场、出场点位
        :param active:
        :return: price
        """
        if active:
            close = self.data['close'].values
            np.append(close, self.current_price)
            ema = talib.EMA(close, timeperiod=timeperiod)  # TODO: 几日均线？
            return ema[-1]
        else:
            high = self.data.iloc[-1]['high']  # 前一日高点/低点
            return high

    def save_zone(self, stock_price):
        """
        安全区法计算仓位
        :return:
        """
        abd, ema22 = avg_break_down(self.data)
        save_part = (self.total_net_worth * 0.02) / (stock_price - ema22 + abd) * stock_price
        save_ratio = save_part / self.total_net_worth
        board_lot = save_part // (stock_price * 100)
        return save_part, save_ratio, board_lot

    def choose(self):  # TODO: 离场
        fs = self._first_screen()
        if fs == 2:
            ss = self._second_screen(active=True)
            if ss:
                price = self._third_screen(True)
                part, ratio, board_lot = self.save_zone(price)
                # return True
                print(f'Suggested buying point: {price:.2f},'
                      f' suggested part: {round(part)}')
                print(ratio, board_lot)
                return price, part, ratio, board_lot


# if __name__ == '__main__':
#     ts = TripleScreen()

