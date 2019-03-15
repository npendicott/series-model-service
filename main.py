from model.series_sample import TimeSeriesSample
from data.energy_service import EnergyService

if __name__ == "__main__":

    service = EnergyService()
    res_frame = service.sample_data('MAC000246', '2012-04-12 10:30:00.0000000', '2012-07-12 10:30:00.0000000')

    #'2012-04-13T00:00:00Z'
    sample = TimeSeriesSample(res_frame, date_fmt_str="%Y-%m-%dT%H:%M:%SZ")
    sample.day_of_week_class()
    sample.train_test_split(20)

    print(sample.base.head())

