import unittest
from unittest.mock import patch
from detector.reader import Reader
import pandas as pd


class TestGetData(unittest.TestCase):
    ''' Test for get_data.py'''

    def test_read_csv_to_df(self):
        ''' 
        get data from traders_data.csv
        dataframe has 1000 rows and 10 columns
        '''

        df = Reader.load_csv_to_df("traders_data.csv")
        self.assertEqual(df.shape, (1000, 10))

    def test_read_csv_to_df_error(self):
        ''' 
        get data from non exists file
        '''
        self.assertRaises(
            ValueError, Reader.load_csv_to_df, "non_existing_file.csv")

    def test_fetch_yahoo_stock_data_to_df(self):
        ''' mock fetch AMZN stock_data from yahoo '''
        with patch('detector.reader.data.DataReader') as mocked_reader:
            mocked_df = pd.DataFrame([1, 2, 3])
            mocked_reader.return_value = mocked_df

            df = Reader.fetch_yahoo_stock_data_to_df(
                "AMZN", '2020-1-1', '2020-1-31')
            mocked_reader.assert_called_with(
                "AMZN", start='2020-1-1', end='2020-1-31', data_source='yahoo')
            self.assertEqual(df.to_dict(), mocked_df.to_dict())

    def test_fetch_yahoo_stock_data_to_df_error(self):
        ''' mock fetch non existed stock_data from yahoo '''
        with patch('detector.reader.data.DataReader') as mocked_reader:
            mocked_df = pd.DataFrame()
            mocked_reader.return_value = mocked_df
            self.assertRaises(ValueError, Reader.fetch_yahoo_stock_data_to_df,
                              "non-existed-data", '2020-1-1', '2020-1-31')
            mocked_reader.assert_called_with(
                "non-existed-data", start='2020-1-1', end='2020-1-31', data_source='yahoo')
