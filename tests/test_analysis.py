import unittest
from unittest.mock import patch, PropertyMock
from detector.analysis import Analysis
import pandas as pd


class TestAnalysis(unittest.TestCase):
    @patch('detector.analysis.Manipulator')
    def setUp(self, mockManipulatorClass):
        '''
        Before each test, mock manipulated data
        '''
        mockManipulator = mockManipulatorClass.return_value
        mockManipulator.trading_start_date = PropertyMock(
            return_value='2020-07-01')
        mockManipulator.trading_end_date = PropertyMock(
            return_value='2020-07-03')
        mockManipulator.manipulate.return_value = self.sample_manipulated_data
        self.analysis = Analysis('sample.csv', ["AMZN"])
        self.assertTrue(mockManipulator.manipulate.called)

    def test_count_suspicious_per_trader(self):
        '''
        Compare the result from count_suspicious_per_trader() with expected result
        '''
        df = self.analysis.count_suspicious_per_trader()
        self.assertEqual(
            df.to_dict(), self.expected_suspicious_traders_data.to_dict())

    def test_count_suspicious_by_country_per_month(self):
        '''
        Compare the result from count_suspicious_by_country_per_month() with expected result
        '''
        df = self.analysis.count_suspicious_by_country_per_month()
        self.assertEqual(
            df.to_dict(), self.expected_suspicious_country_data.to_dict())

    @property
    def sample_manipulated_data(self):
        '''
        For mock: 5 rows of manipulated data, 4 are suspicious 
        (1 not on trading date for the stock, 3 are outside of price range of the day)
        '''
        columns = ['countryCode', 'name', 'traderId', 'stockSymbol',
                   'stockName', 'price', 'tradeDate', 'Symbols', 'Date', 'High', 'Low']
        data = [['UZ', 'Brandi Robbins', 'JTzVqzzIkFlrYUQbhnOR', 'AMZN', 'Amazon', 1857.63056, '2020-07-01', 'AMZN', '2020-07-01', 2895.0, 2754.0],
                ['BT', 'Allison Davis', 'TzqyQTQjZGeLZuJqlLaQ', 'AMZN', 'Amazon', 2078.4403,
                    '2020-07-02', 'AMZN', '2020-07-02', 2955.56005859375, 2871.10009765625],
                ['BT', 'Allison Davis', 'TzqyQTQjZGeLZuJqlLaQ', 'AMZN', 'Amazon', 2103.0,
                    '2020-07-02', 'AMZN', '2020-07-02', 2955.56005859375, 2871.10009765625],
                ['NZ', 'Brittany Herring', 'pjjFIyeNTWRUWCuKoQSU', 'AMZN',
                    'Amazon', 2351.144499636, '2020-07-03', None, None, None, None],
                ['CV', 'April Floyd', 'stOzTFyGrgJGPgVPVTJQ', 'AMZN', 'Amazon', 2784.0, '2020-07-01', 'AMZN', '2020-07-01', 2895.0, 2754.0]]

        df = pd.DataFrame(data, columns=columns)
        df.tradeDate = pd.to_datetime(df.tradeDate)
        df.Date = pd.to_datetime(df.Date)

        df.countryCode = df.countryCode.astype(
            'category')
        df.stockSymbol = df.stockSymbol.astype(
            'category')
        df.Symbols = df.Symbols.astype(
            'category')

        return df

    @property
    def expected_suspicious_traders_data(self):
        '''
        For mock: expected result data for count_suspicious_per_trader()
        '''
        index = [1, 2, 3]
        columns = ['traderId', 'name', 'suspicious']
        data = [['TzqyQTQjZGeLZuJqlLaQ', 'Allison Davis', 2],
                ['JTzVqzzIkFlrYUQbhnOR', 'Brandi Robbins', 1],
                ['pjjFIyeNTWRUWCuKoQSU', 'Brittany Herring', 1]]

        df = pd.DataFrame(data, index=index, columns=columns)
        df.index.name = 'rank'
        return df

    @property
    def expected_suspicious_country_data(self):
        '''
        For mock: expected result data for count_suspicious_by_country_per_month()
        '''
        index = ['BT', 'NZ', 'UZ', 'CV']
        columns = ['2020-07', 'total']
        data = [[2, 2], [1, 1], [1, 1], [0, 0]]

        df = pd.DataFrame(data, index=index, columns=columns)
        df.index.name = 'country code'
        df.columns.name = 'month'
        return df
