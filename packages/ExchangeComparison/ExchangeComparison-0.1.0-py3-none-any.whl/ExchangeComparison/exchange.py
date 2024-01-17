from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

class Exchange():
    def __init__(self, money_kind='USDJPY') -> None:
        print(f'Kind of money : {money_kind}')
        print('Data from 1996-10-30 to latest is read in.')
        self.date = ""
        self.days = 0
        self.choozed_array = np.array([])
        # 最新のデータを持ってくる
        start_date = "1996-10-30"
        self.end_date = datetime.now().date()
        historical_close_prices = self.fx_rates(f"{money_kind}=X", start_date, self.end_date)

        value_list = np.array(historical_close_prices)
        date_list = historical_close_prices.index.values
        index_list = np.array([str(i)[:10] for i in date_list[1:]])

        date1 = date_list[1:]
        date2 = date_list[:-1]
        value1 = value_list[1:]
        value2 = value_list[:-1]
        stock_value = value1 - value2

        stock_date = np.array([])

        for time1, time2 in zip(date1,date2):
            # 日時の差を計算
            time_difference = np.timedelta64(time1 - time2, 'ns')
            # 差を日に変換
            days_difference = time_difference.astype(float) / (24 * 60 * 60 * 10**9)
            stock_date = np.append(stock_date,days_difference)
        self.stock_array = np.vstack((index_list, stock_date, stock_value, value_list[1:]))
        
        print('ready')

    def fx_rates(self, ticker, start_date, end_date):
        # 指定された日付範囲の終値データを取得
        historical_data = yf.Ticker(ticker).history(start=start_date, end=end_date)
        # 終値列を返す（DataFrameの最初の列が終値）
        return historical_data['Close']
    
    def calculation(self,split_array):
        for i in range(0, len(split_array[0]), self.days):
            start_id = i
            stop_id = i + self.days
            current_array = split_array[:, start_id:stop_id]

            if len(current_array[0]) == self.days:
                sum_value = 0
                for j in range(self.days):
                    sum_value += np.linalg.norm(np.array(self.choozed_array[1:3,j],dtype=float) - np.array(current_array[1:3,j], dtype=float))
                self.calculation_dict[current_array[0][0]] = sum_value/self.days

    def plot_rate(self, near_array):
        plt.figure(figsize=(12, 8))
        plt.plot(near_array[2], label='similar rate',marker='o', linestyle='-')
        plt.plot(self.choozed_array[2], label='choice rate', color='orange', marker='o', linestyle='--', alpha=0.7, linewidth=0.8)
        plt.title(f'USD/JPY Exchange Rate ( {near_array[0][0]} ~ {near_array[0][-1]} )')
        plt.xlabel('Date')
        plt.ylabel('Exchange Rate')
        plt.yticks([])
        plt.grid(True)
        plt.legend()
        plt.show()
    
    def get_exchange(self, date='Today', days=20):
        if date == 'Today':
            self.date = self.stock_array[0][-1]
        else:
            self.date = date
        self.days = days
        
        self.calculation_dict = {}
        # 抜く部分を探す
        indices = np.where(self.stock_array[0] == self.date)
        if len(indices[0]) <= 0:
            print('Do not have date. please choice another date.')
            return
        indices = indices[0][0]+1
        # 切り抜く
        self.choozed_array = self.stock_array[:, indices-days : indices]

        # 抜いた部分を消す
        delete_array = np.delete(self.stock_array, slice(indices - days, indices), axis=1)
        split1_array = delete_array[:, :indices - days]
        split2_array = delete_array[:, indices - days:]
        self.calculation(split1_array)
        self.calculation(split2_array)
        
        sorted_items = sorted(self.calculation_dict.items(), key=lambda x: x[1])[:4]
        
        for key, value in sorted_items:
            search_id = np.where(self.stock_array[0] == key)
            search_id = search_id[0][0]
            near_array = self.stock_array[:, search_id : search_id + days]
            print('類似度：',value)
            self.plot_rate(near_array)
            print('------'*10)

if __name__ == "__main__":
    e = Exchange()
    e.get_exchange()