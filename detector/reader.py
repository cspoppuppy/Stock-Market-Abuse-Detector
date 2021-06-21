import pandas as pd
from pandas_datareader import data


class Reader():
    '''
    Data reader to get data from data sources
    '''
    @classmethod
    def load_csv_to_df(cls, filename):
        '''
        Get data from csv file to pandas dataframe
        '''
        df = pd.DataFrame()
        try:
            df = pd.read_csv(filename)
        except:
            print("Fail to read data from {}".format(filename))
        if df.empty:
            raise ValueError("No data available")
        return df

    @classmethod
    def fetch_yahoo_stock_data_to_df(cls, stock_syms, start_date, end_date):
        '''
        start_date: YYYY-MM-DD
        end_date: YYYY-MM-DD

        Get stocks daily pricing data within date range according to stock symbols provided
        '''
        df = pd.DataFrame()
        try:
            df = data.DataReader(stock_syms, start=start_date,
                                 end=end_date, data_source='yahoo')
        except:
            print("Fail to fetch data from yahoo for stock {} between {} - {}".format(
                stock_syms, start_date, end_date))
        if df.empty:
            raise ValueError("No data available")
        return df
