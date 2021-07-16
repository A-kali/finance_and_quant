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
}


class StockPool:
    save_name = 'stocks_pool.csv'
    def __init__(self):
        self.data = pd.read_csv(self.save_name)

    def add(self, code):
        ashare = AShare()
        name = ashare[code[:6]]['name']
        if name not in self.data['name'].values.tolist():
            self.data = self.data.append({'code': code, 'name': name}, ignore_index=True)
            self.data.to_csv(self.save_name, index=False)
        else:
            print(f'{code} is already included')

    def __getitem__(self, item):
        return self.data.iloc[item]

    def __iter__(self):
        return self.data.iterrows()


class AShare:
    def __init__(self):
        save_path = '.'
        str_date = latest_trading_day()
        f_name = f'{save_path}/ashares_{str_date}.csv'
        if not os.path.exists(f_name):
            data = ak.stock_zh_a_spot_em()
            data.rename(columns=english_columns, inplace=True)
            for f in glob.glob(f'{save_path}/ashares_*.csv'):
                os.remove(f)
            print(f_name)
            data['code'].to_string()
            data.set_index('code', inplace=True)
            data.to_csv(f_name)
        else:
            data = pd.read_csv(f_name, index_col='code')

        self.data = data

    def __getitem__(self, code):
        return self.data.loc[code]


if __name__ == '__main__':
    sp = StockPool()
    sp.add('603288')