import unittest

# I wish I could keep these tests at the module level, but the import statements are breaking
from model import series_sample
from model.series_sample import TimeSeriesSample
import json

# TODO: Is this bad? To have to import the test_target's dependencies?
import pandas
from datetime import datetime


# TODO: Comment tests
class TestSeriesSample(unittest.TestCase):

    @staticmethod
    def parse_test_data():
        test_data_path = './test/test_data.json'
        with open(test_data_path) as json_file:
            res_json = json.load(json_file)

            result_series = res_json['Results'][0]['Series'][0]

            table = result_series['name']

            columns = result_series['columns']
            columns = columns[1:]  # Drop index label

            values = result_series['values']
            data = [value[1:] for value in values]
            index = [value[0] for value in values]

            return table, columns, index, data

    def init_test_sample(self):
        table, columns, index, data = self.parse_test_data()

        sample = TimeSeriesSample(data=data, columns=columns,  # Super
                                  datetime_index=index,
                                  categorical_features=['cat', 'features'])  # RYO
        return sample

    # Init tests
    def test_init(self):
        test_series_sample = self.init_test_sample()

        self.assertEqual(True, True, "T")

    # Train/Test Split Checks
    def test_train_test_split_result_size(self):
        sample = self.init_test_sample()

        sample.valid_split(20)

        self.assertEqual(len(sample), 16)
        self.assertEqual(len(sample.validation_set), 4)

    def test_train_test_split_invalid_percent(self):
        sample = self.init_test_sample()

        self.assertRaises(ValueError, sample.valid_split, 101)
        self.assertRaises(ValueError, sample.valid_split, -1)


    # def test_index_datetime_unparsable(self):
    #     test_frame = self.setup_test_frame()
    #
    #     self.assertRaises(TypeError, TimeSeriesSample, test_frame, 'good_key')
    #
    # def test_default_index_datetime_parse(self):
    #     sample = self.setup_test_sample()
    #
    #     first_index = sample.base.index[0]
    #
    #     self.assertIsInstance(first_index, datetime)
    #

