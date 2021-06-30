from .manipulator import Manipulator
import pandas as pd

pd.options.mode.chained_assignment = None


class Analysis():
    '''
    Analysis on manipulated data

    - count_suspicious_per_trader()
    - count_suspicious_by_country_per_month()
    '''

    def __init__(self, filename, stock_symbols=[]):
        '''
        (str, list) -> NoneType

        Get suspicious data
        '''
        self.stock_symbols = stock_symbols
        self.data = self.__get_data_for_analysis(
            filename)

    def __get_data_for_analysis(self, filename):
        '''
        (str) -> pandas DataFrame

        Keep suspicious records, start date and end date from manipulated data
        '''
        self.__get_manipulated_data(filename)
        suspicious = self.__get_suspicious(self.manipulated)
        return suspicious

    def __get_manipulated_data(self, filename):
        '''
        (str)

        Get manipulated data
        '''
        manipulator = Manipulator(filename, self.stock_symbols)
        # Get date range from data
        self.start_date = manipulator.trading_start_date
        self.end_date = manipulator.trading_end_date
        # Get cleaned and transformed data
        self.manipulated = manipulator.manipulate()

    @staticmethod
    def __get_suspicious(data):
        '''
        (pandas DataFrame) -> pandas DataFrame

        Keep suspicious data, add suspicious column with value 1
        '''
        # Mark suspicious
        # 1. Not a trading date for the stock - missing Data values from yahoo
        # 2. Price is outside of the trading price range in the day

        # Series of true or false
        suspicious = data.Date.isnull() | (
            data.price > data.High) | (data.price < data.Low)
        # Filter data by suspicious
        data = data[suspicious]
        # Create new column suspicious and put value as 1
        data.loc[:, 'suspicious'] = 1
        return data

    def count_suspicious_per_trader(self):
        '''
        () -> pandas DataFrame

        List suspicious trades by traders in descending order (return pandas data frame)
        '''
        # sum suspicious trades group by trader and sort in descending order
        grouped = self.__group_suspicious_data(
            self.data, ['traderId', 'name'])

        grouped = grouped.sort_values(ascending=False)
        # convert to data frame
        data = grouped.to_frame().reset_index()
        # index starts from 1
        data.index += 1
        # name index as rank
        data.index.name = "rank"
        return data

    def count_suspicious_by_country_per_month(self):
        '''
        () -> pandas DataFrame

        List suspicious trades by country per month (return pandas data frame)
        '''
        # sum suspicious trades group by tradeDate and country and sort in descending order
        grouped = self.__group_suspicious_data(
            self.data, ['tradeDate', 'countryCode'])
        # Group data monthly
        monthly = self.__group_suspicious_data(grouped.to_frame(), [pd.Grouper(
            level='tradeDate', freq='M'), pd.Grouper(level='countryCode')])
        # Pivot the months
        data = monthly.to_frame().unstack(level='tradeDate')
        # format data frame headers
        data.columns, data.index = self.__format_country_headers(
            data.columns, data.index)
        # add total column
        data['total'] = data.sum(axis=1)
        # sort data frame by total descending
        data = data.sort_values('total', ascending=False)
        return data

    @staticmethod
    def __group_suspicious_data(data, groupers):
        '''
        (pandas DataFrame, list) -> pandas DataFrameGroupBy

        Group data frame by groupers, and sum suspicious
        '''
        return data.groupby(
            groupers).suspicious.sum()

    @staticmethod
    def __format_country_headers(columns, index):
        '''
        (pandas Index, pandas Index) -> Tuple of pandas Index

        Format and remane column headers and index
        '''
        # drop top level index
        new_cols = columns.droplevel(0)
        # format headers as YYYY-MM
        columns = new_cols.map(lambda x: x.strftime('%Y-%m'))
        # rename column index
        columns.name = "month"
        # rename index (row)
        index.name = "country code"
        return columns, index
