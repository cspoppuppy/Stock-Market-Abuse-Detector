import unittest
from unittest.mock import patch
from detector.manipulator import Manipulator
import pandas as pd


class TestManipulator(unittest.TestCase):
    def setUp(self):
        '''
        Before each test, mock a sample csv file data
        '''
        with patch('detector.manipulator.Reader.load_csv_to_df') as mock_load_csv_to_df:
            mock_load_csv_to_df.return_value = self.sample_traders_data
            self.manipulator = Manipulator('sample.csv', ["AMZN"])
            mock_load_csv_to_df.assert_called_with(
                'sample.csv')

    def test_trading_start_date(self):
        '''
        Test the earliest date from sample data should be 2020-07-01
        '''
        start_date = self.manipulator.trading_start_date
        self.assertEqual(start_date, '2020-07-01')

    def test_trading_end_date(self):
        '''
        Test the latest date from sample data should be 2020-07-03
        '''
        end_date = self.manipulator.trading_end_date
        self.assertEqual(end_date, '2020-07-03')

    def test_manipulate(self):
        '''
        After manipulate, the new data set should remove the 2 rows of bad data from traders and merge with stocks data
        New size should be 5 rows and 11 columns
        '''
        with patch('detector.reader.Reader.fetch_yahoo_stock_data_to_df') as mock_fetch_yahoo_stock_data_to_df:
            mock_fetch_yahoo_stock_data_to_df.return_value = self.sample_stocks_data
            df = self.manipulator.manipulate()
            self.assertEqual(df.shape, (5, 11))

    @property
    def sample_traders_data(self):
        '''
        For mock: 7 rows of data between 2020-07-01 and 2020-07-03
        2 lines of dirty data (no stockSymbol, tradeId, tradeDatetime)

        '''
        columns = ['countryCode', 'firstName', 'lastName', 'traderId',
                   'stockSymbol', 'stockName', 'tradeId', 'price', 'volume', 'tradeDatetime']
        data = [['UZ', 'Brandi', 'Robbins', 'JTzVqzzIkFlrYUQbhnOR', 'AMZN', 'Amazon', 'X0-7401234c', 1857.63056, None, '2020-07-01 07:18:39'],
                ['BT', 'Allison', 'Davis', 'TzqyQTQjZGeLZuJqlLaQ', 'AMZN',
                 'Amazon', 'K3-3189326K', 2078.4403, 32.0, '2020-07-02 13:59:03'],
                ['BT', 'Allison', 'Davis', 'TzqyQTQjZGeLZuJqlLaQ', 'AMZN',
                 'Amazon', None, 2103.0, 295.0, '2020-07-02 10:38:03'],
                ['NZ', 'Brittany', 'Herring', 'pjjFIyeNTWRUWCuKoQSU', 'AMZN', 'Amazon',
                 'U9-4261680I', 2351.144499636, 154.0, '2020-07-03 17:42:11'],
                ['GT', 'Holly', 'Simmons', 'puCpymcjBdurvfVyRYry', 'AMZN',
                 'Amazon', 'e3-5475253C', 2364.335, 144.0, None],
                ['CV', 'April', 'Floyd', 'stOzTFyGrgJGPgVPVTJQ', 'AMZN',
                 'Amazon', 'E1-1662257k', 2784.0, 261.0, '2020-07-01 19:58:35'],
                [None, None, None, None, None, None, 'b0-7662558U', 1596.1, 19.0, '2020-07-02 11:36:01']]

        return pd.DataFrame(data, columns=columns)

    @property
    def sample_stocks_data(self):
        '''
        For mock: 2 rows of data on 2020-07-01 and 2020-07-02
        '''
        index = ['2020-07-01', '2020-07-02']
        columns = [('Adj Close', 'AMZN'), ('Close', 'AMZN'), ('High', 'AMZN'),
                   ('Low', 'AMZN'), ('Open', 'AMZN'), ('Volume', 'AMZN')]

        columns = pd.MultiIndex.from_tuples(
            columns, names=["Attributes", "Symbols"])
        data = [[2878.699951171875, 2878.699951171875, 2895.0, 2754.0, 2757.989990234375, 6363400],
                [2890.300048828125, 2890.300048828125, 2955.56005859375, 2871.10009765625, 2912.010009765625, 6593400]]

        df = pd.DataFrame(data, index=pd.to_datetime(
            index), columns=columns)
        df.index.name = "Date"

        return df
