import unittest

# I wish I could keep these tests at the module level, but the import statements are breaking
from model import series_sample
from model.series_sample import TimeSeriesSample

# TODO: Is this bad? To have to import the test_target's dependencies?
import pandas
from datetime import datetime


# TODO: Comment tests
class TestSeriesSample(unittest.TestCase):

    @staticmethod
    def setup_test_frame():
        # TODO: Is something like this neccissarry, or should I just let it fail as is??
        test_data_path = './data/test_data.csv'
        try:
            return pandas.read_csv(test_data_path)
        except FileNotFoundError:
            raise FileNotFoundError("Can't find the test data file at {0}".format(test_data_path))

    def setup_test_sample(self):
        test_frame = self.setup_test_frame()
        return TimeSeriesSample(test_frame, 'datetime')

    # Init tests
    def test_init_index_key(self):
        test_frame = self.setup_test_frame()

        self.assertRaises(KeyError, TimeSeriesSample, test_frame, 'bad_key')

    def test_index_datetime_unparsable(self):
        test_frame = self.setup_test_frame()

        self.assertRaises(TypeError, TimeSeriesSample, test_frame, 'good_key')

    def test_default_index_datetime_parse(self):
        sample = self.setup_test_sample()

        first_index = sample.base.index[0]

        self.assertIsInstance(first_index, datetime)

    # Train/Test Split Checks
    def test_train_test_split_result_size(self):
        sample = self.setup_test_sample()

        sample.train_test_split(20)

        self.assertEqual(len(sample.base), 16)
        self.assertEqual(len(sample.base_valid), 4)

    def test_train_test_split_invalid_percent(self):
        # test_frame = pandas.read_csv('./data/test_data.csv')
        sample = self.setup_test_sample()

        self.assertRaises(ValueError, sample.train_test_split, 101)
        self.assertRaises(ValueError, sample.train_test_split, -1)


# if __name__ == '__main__':
#     dataframe = pandas.read_csv('./data/test_data.csv')
#     decomp = series_sample.TimeSeriesSample(dataframe, 'testing')
#     print(dataframe.head())

