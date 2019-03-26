from data.energy_service import EnergyService

from pandas import DataFrame
from model.series_sample import TimeSeriesSampleAccessor

import json
import os


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


def init_test_sample():
    table, timestamps, columns, data = parse_test_data()
    # table, columns, index, data = parse_test_data()

    frame = DataFrame(data=data, columns=columns)
    frame['timestamp'] = timestamps

    # sample = TimeSeriesSample(data=data, columns=columns,  # Super
    #                           datetime_index=index,
    #                           # valid_percent=20,
    #                           categorical_features=['cat', 'features'])  # RYO

    return frame


if __name__ == "__main__":
    # PROD
    service = EnergyService()

    table, timestamps, lables, data = service.daily_reading("MAC000246", "2011-04-12 10:30:00.0000000", "2012-04-12 10:30:00.0000000")
    # table, timestamps, columns, data = service.sample_data('MAC000246', '2012-04-12 10:30:00.0000000', '2012-05-12 10:30:00.0000000')

    sample = DataFrame(data=data, columns=lables)
    sample['timestamp'] = timestamps

    print(sample.head())

    # TEST
    # sample = init_test_sample()

    sample.tss.format_index()

    subsample = sample[2:4]
    print(len(subsample))

    sample.tss.day_of_week_class()

    stationality = sample.tss.stationality('energy_mean')

    auto_corr = sample.tss.autocorrelation('energy_mean')

    print()





















    #
    #
    #
    # service = EnergyService()
    # # res_frame = service.sample_data('MAC000246', '2012-04-12 10:30:00.0000000', '2012-07-12 10:30:00.0000000')
    # table, columns, index, data = service.sample_data('MAC000246', '2012-04-12 10:30:00.0000000', '2012-07-12 10:30:00.0000000')
    #
    # # frame = DataFrame(data=res_frame)
    # #frame.head()
    # #'2012-04-13T00:00:00Z'
    #
    # sample = TimeSeriesSample(data=data,  columns=columns,  # Super
    #                           datetime_index=index,
    #                           # valid_percent=20,
    #                           categorical_features=['cat', 'features'])  # RYO
    #
    # print("Initial")
    # sample.print()
    # # print(len(sample))
    # # print(sample.tail())
    # # print(sample.train_test_split_index)
    # # print(sample.categorical_features)
    # # print(sample.validation_set)
    #
    #
    # sample.valid_split(20)
    # # sample.weekend_weekday_class()
    #
    # print("Post Split")
    # sample.print()
    # # print(len(sample))
    # # print(sample.tail())
    # # print(sample.train_test_split_index)
    # # print(sample.categorical_features)
    # # print(len(sample.validation_set))
    #
    #
    # print()
    #
