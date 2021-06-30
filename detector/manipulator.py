from .reader import Reader
import pandas as pd

pd.options.mode.chained_assignment = None


class Manipulator():
    '''
    Data manipulator - clean up and merge data
    '''

    def __init__(self, traders_data_file, stock_symbols=[]):
        '''
        (str, list) -> NoneType

        initialise with traders data
        '''
        self.stock_symbols = stock_symbols
        # Get traders data
        self.traders_data_df = self.__get_traders_data_from_csv(
            traders_data_file)

    def __get_traders_data_from_csv(self, traders_data_file):
        '''
        (str) -> pandas DataFrame

        Get data from csv file and transform
        '''
        # Read data from csv file
        raw_traders_data_df = Reader.load_csv_to_df(traders_data_file)
        # Return transformed data
        return self.__process_traders_data(raw_traders_data_df, self.stock_symbols)

    @staticmethod
    def __process_traders_data(raw_traders_data_df, stock_symbols):
        '''
        (pandas DataFrame, list) -> pandas DataFrame

        Transform traders data from CSV file
        '''
        # ----------------------------------------------------------------
        # Filter out bad data
        # ----------------------------------------------------------------
        # Remove rows without stockSymbol, traderId, or tradeDatetime
        traders_data_df = raw_traders_data_df[raw_traders_data_df.stockSymbol.notnull(
        ) & raw_traders_data_df.traderId.notnull(
        ) & raw_traders_data_df.tradeDatetime.notnull(
        )]
        # ----------------------------------------------------------------
        # Keep selected stocks only if provided, otherwise show all stocks
        # ----------------------------------------------------------------
        if stock_symbols:
            traders_data_df = traders_data_df[traders_data_df.stockSymbol.isin(
                stock_symbols)]
        # ----------------------------------------------------------------
        # Transform data
        # ----------------------------------------------------------------
        # Format countryCode and stockSymbol columns as category for better performance
        traders_data_df.loc[:, 'countryCode'] = traders_data_df.countryCode.astype(
            'category')
        traders_data_df.loc[:, 'stockSymbol'] = traders_data_df.stockSymbol.astype(
            'category')
        # Create new tradeDate column with datetime type
        # truncate to date
        traders_data_df.loc[:, 'tradeDate'] = pd.to_datetime(
            traders_data_df.tradeDatetime).dt.date
        # Convert to datetime type
        traders_data_df.loc[:, 'tradeDate'] = pd.to_datetime(
            traders_data_df.tradeDate, format='%Y-%m-%d')
        # Combine firstName and lastName
        traders_data_df.loc[:, 'name'] = traders_data_df.firstName + \
            ' ' + traders_data_df.lastName

        return traders_data_df[['countryCode', 'name', 'traderId', 'stockSymbol', 'stockName', 'price', 'tradeDate']]

    def __get_stocks_list(self):
        '''
        () -> list

        Get an unique list of stock symbols from traders data
        '''
        return self.traders_data_df.stockSymbol.unique()

    @property
    def trading_start_date(self):
        '''
        () -> str: YYYY-MM-DD

        Get the earliest trade date from traders data
        '''
        return self.traders_data_df.tradeDate.min().strftime('%Y-%m-%d')

    @property
    def trading_end_date(self):
        '''
        () -> str: YYYY-MM-DD

        Get the latest trade date from traders data
        '''
        return self.traders_data_df.tradeDate.max().strftime('%Y-%m-%d')

    def __fetch_stocks_data_from_yahoo(self):
        '''
        () -> pandas DataFrame

        Get stocks daily pricing data from yahoo
        for stocks exist in traders data
        and limit the date range according to traders data
        '''
        stocks_list = self.__get_stocks_list()
        start_date = self.trading_start_date
        end_date = self.trading_end_date
        # Get stocks information from yahoo, according to the list of stocks symbol, start date and end date
        raw_stock_data = Reader.fetch_yahoo_stock_data_to_df(
            stocks_list, start_date, end_date)

        return self.__process_stocks_data(raw_stock_data)

    @staticmethod
    def __process_stocks_data(raw_stocks_data_df):
        '''
        (pandas DataFrame) -> pandas DataFrame

        Transform raw stocks data from yahoo
        '''
        # unpivot data
        stocks_data_df = raw_stocks_data_df.stack(level='Symbols')
        # swap index levels and sort data
        stocks_data_df = stocks_data_df.swaplevel(0, 1).sort_index()
        # remove empty rows if any
        stocks_data_df = stocks_data_df.dropna(how="all")
        # reset index
        stocks_data_df = stocks_data_df.reset_index()
        # Format Symbols column as category for better performance
        stocks_data_df.loc[:, 'Symbols'] = stocks_data_df.Symbols.astype(
            'category')
        # Keep columns needed
        return stocks_data_df[['Symbols', 'Date', 'High', 'Low']]

    def manipulate(self):
        '''
        () -> pandas DataFrame

        Produce a clean set of of merged traders data and Yahoo stocks data (return pandas dataframe)
        '''
        # raise error if there is no valid traders data or stocks data after data transform
        if not self.traders_data_df.empty:
            stocks_data_df = self.__fetch_stocks_data_from_yahoo()
            if stocks_data_df.empty:
                raise ValueError("No valid data")

            return self.__join_traders_and_stocks_data(self.traders_data_df, stocks_data_df)
        else:
            raise ValueError("No valid data")

    @staticmethod
    def __join_traders_and_stocks_data(traders_data_df, stocks_data_df):
        '''
        (pandas DataFrame, pandas DataFrame) -> pandas DataFrame

        Merge traders and stocks data
        '''
        joined_df = pd.merge(traders_data_df, stocks_data_df, left_on=[
                             'stockSymbol', 'tradeDate'], right_on=['Symbols', 'Date'], how='left')
        return joined_df
