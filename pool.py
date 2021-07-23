import os
import glob
import pandas as pd
import akshare as ak

from utils import latest_trading_day

english_columns = {
    '序号': 'id',
    '代码': 'code',
    '名称': 'name',
    '成交量': 'volume',
    '最高': 'high',
    '最低': 'low',
    '开盘': 'open',
    '收盘': 'close',
    '最新价': 'price',
}


class StockPool:
    save_name = 'stocks_pool.csv'
    def __init__(self):
        self.stocks = pd.read_csv(self.save_name, dtype='object').set_index('code')
        self.ashare = AShare()
        self.stocks['price'] = self.ashare[self.ashare.data.index.isin(self.stocks.index)]['price']
        self.stocks.reset_index(inplace=True)

    def add(self, code):
        name = self.ashare[code[:6]]['name']
        if name not in self.stocks['name'].values.tolist():
            self.stocks = self.stocks.append({'code': code, 'name': name}, ignore_index=True)
            self.stocks.to_csv(self.save_name, index=False)
            print(f'added: {code} {name}')
        else:
            print(f'{code} is already included')

    def __getitem__(self, item):
        return self.stocks.iloc[item]

    def __iter__(self):
        return self.stocks.iterrows()


class AShare:
    def __init__(self):
        # save_path = '.'
        # str_date = latest_trading_day()
        # f_name = f'{save_path}/ashares_{str_date}.csv'
        # if not os.path.exists(f_name):
        # 获取所有A股当前信息
        if 0:  # debug
            data = pd.read_csv('ashares_20210720.csv', dtype='object')
        else:
            data = ak.stock_zh_a_spot_em()
        data.rename(columns=english_columns, inplace=True)
        # for f in glob.glob(f'{save_path}/ashares_*.csv'):
        #     os.remove(f)
        # print(f_name)
        # data.set_index('code', inplace=True)
        # data.to_csv(f_name)
        # else:
        #     data = pd.read_csv(f_name, dtype='object')
        #     data.set_index('code', inplace=True)
        self.data = data.set_index('code')

    def __getitem__(self, code):
        return self.data.loc[code]



if __name__ == '__main__':
    sp = StockPool()
    sp.add('603288')