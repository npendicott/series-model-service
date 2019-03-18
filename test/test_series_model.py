import unittest

from pandas import DataFrame
from model.series_model import TimeSeriesModelAccessor

import json


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
            timestamps = [value[0] for value in values]

            return table, timestamps, columns, data

    def init_test_sample(self):
        table, timestamps, columns, data = self.parse_test_data()

        frame = DataFrame(data=data, columns=columns)
        frame['timestamp'] = timestamps

        return frame

    # Init tests
    def test_init(self):
        sample = self.init_test_sample()

        self.assertEqual(True, True, "T")

    def test_index_fmt(self):
        sample = self.init_test_sample()

        sample.tsm.format_index()

        # TODO: Index Checks
        self.assertEqual(True, True)

    # Stationality
    def test_stationality_adf(self):
        sample = self.init_test_sample()

        sample.tsm.format_index()

        result = sample.tsm.stationality('energy_mean')

        # TODO: Build Dict
        # result['adf'] = adf_result[0]
        # result['pvalue'] = adf_result[1]
        # result['usedlag'] = adf_result[2]
        # result['nobs'] = adf_result[3]
        # result['values'] = adf_result[4]
        # result['icbest'] = adf_result[5]

    # # Train/Test Split Checks
    # def test_train_test_split_result_size(self):
    #     sample = self.init_test_sample()
    #
    #     sample.valid_split(20)
    #
    #     self.assertEqual(len(sample), 16)
    #     self.assertEqual(len(sample.validation_set), 4)
    #
    # def test_train_test_split_invalid_percent(self):
    #     sample = self.init_test_sample()
    #
    #     self.assertRaises(ValueError, sample.valid_split, 101)
    #     self.assertRaises(ValueError, sample.valid_split, -1)


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


