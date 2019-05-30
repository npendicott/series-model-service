from data.energy_service import EnergyService

from pandas import DataFrame
from model.series_sample import TimeSeriesSampleAccessor

# Schema
from data.schemas.influx_schema import DailyReadingSchema, HHourlyReadingSchema, SolarControlSchema, SolarPandOSchema

import json
import os

INFLUX_TS_FMT = "%Y-%m-%dT%H:%M:%SZ"

# TODO: Figure out Index
#   Only need MultiIndex if I can't split like [x:y]
#   I could either extract from some internal Series w/ a key and fmt string, or take external

# TODO: Clean up the junk

# TODO: EnergyService probably needs a look

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

    frame = DataFrame(data=data, columns=columns)
    frame['timestamp'] = timestamps

    return frame


if __name__ == "__main__":
    # PROD
    service = EnergyService()

    # London
    res = service.get_readings("daily", "MAC000246", "2011-04-12 10:30:00.0000000", "2012-04-12 10:30:00.0000000")
    # table, timestamps, columns, data = service.sample_data('MAC000246', '2012-04-12 10:30:00.0000000', '2012-05-12 10:30:00.0000000')
    # table, timestamps, lables, data = service.hhourly_reading("MAC000246", "2011-04-12 10:30:00.0000000", "2012-04-12 10:30:00.0000000")

    # Solar
    # table, timestamps, lables, data = service.get_readings("control", "", "2015-04-15 18:00:00", "2015-04-15 19:16:18")

    table, timestamps, lables, data = service.parse_response(res, DailyReadingSchema())

    sample = DataFrame(data=data, columns=lables)
    sample['timestamp'] = timestamps

    print(sample.describe())
    print(sample.head())

    sample.tss.format_index(timestamps, INFLUX_TS_FMT)

    subsample = sample[2:4]
    print(len(subsample))

    sample.tss.day_of_week_class()

    # stationality = sample.tss.stationality('energy_mean')
    #
    # auto_corr = sample.tss.autocorrelation('energy_mean')

    stationality = sample.tss.stationality('power')

    auto_corr = sample.tss.autocorrelation('power')

    print(auto_corr)
    print()
