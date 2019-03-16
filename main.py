from model.series_sample import TimeSeriesSample
from data.energy_service import EnergyService

from pandas import DataFrame

if __name__ == "__main__":

    service = EnergyService()
    # res_frame = service.sample_data('MAC000246', '2012-04-12 10:30:00.0000000', '2012-07-12 10:30:00.0000000')
    table, columns, index, data = service.sample_data('MAC000246', '2012-04-12 10:30:00.0000000', '2012-07-12 10:30:00.0000000')

    # frame = DataFrame(data=res_frame)
    #frame.head()
    #'2012-04-13T00:00:00Z'

    sample = TimeSeriesSample(data=data, index=index, columns=columns,  # Super
                              valid_percent=20, categorical_features=['cat', 'features'])  # RYO

    print("Initial")
    sample.print()
    # print(len(sample))
    # print(sample.tail())
    # print(sample.train_test_split_index)
    # print(sample.categorical_features)
    # print(sample.validation_set)


    sample.valid_split(20)

    print("Post Split")
    sample.print()
    # print(len(sample))
    # print(sample.tail())
    # print(sample.train_test_split_index)
    # print(sample.categorical_features)
    # print(len(sample.validation_set))


    print()

