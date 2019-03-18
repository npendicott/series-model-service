from pandas import Timestamp, DatetimeIndex, MultiIndex, RangeIndex
from pandas.api.extensions import register_dataframe_accessor

from statsmodels.tsa.stattools import adfuller

# from model.ryo_analysis import kpss_test, quick_autocorr

# import numpy as np
# from pandas import Series, DataFrame, DatetimeIndex
# from datetime import datetime
# from statsmodels.tsa.stattools import adfuller
# from statsmodels.tsa.seasonal import seasonal_decompose
#
# from model.ryo_analysis import kpss_test, quick_autocorr


@register_dataframe_accessor("tsm")
class TimeSeriesModelAccessor:
    """ Adding accessor for some common time series modeling tasks to pandas DataFrame.

    IMPORTANT: So here, we are pretty much creating two indices, a datetime and an int range.
    Pandas has some support for multiple indices, but the whole [0][1] is not my fave.
    So, I guess the choice here is: do we maintain multiple indices??


    http://pandas.pydata.org/pandas-docs/stable/development/extending.html#extending-subclassing-pandas
    http://pandas.pydata.org/pandas-docs/stable/development/extending.html#extending-register-accessors

    This is a good example apparently: https://github.com/geopandas/geopandas/blob/master/geopandas/geodataframe.py
    """
    INFLUX_TS_FMT = "%Y-%m-%dT%H:%M:%SZ"

    # CREATE/CHECK DataFrame
    # TODO: Is there a reason for a static validate?
    #  Should I interanlize/automate the index validation?
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        # TODO: Validate MultiIndex structure
        if not isinstance(obj.index, MultiIndex):
            if 'timestamp' not in obj.columns:
                raise TypeError("Index must be correctly formatted or contain a 'timestamp' column.")

    def format_index(self):
        datetime_index_key = 'timestamp'

        timestamps = [Timestamp.strptime(ts, self.INFLUX_TS_FMT) for ts in self._obj[datetime_index_key]]
        timestamp_index = DatetimeIndex(timestamps)
        # print(timestamp_index)

        int_index = self._obj.index
        # print(int_index)

        self._obj.set_index([int_index, timestamp_index], inplace=True)

        # Clea up
        # TODO: Where does the timestamp column go? Getting a KeyError
        # self._obj.drop(datetime_index_key, inplace=True)

        # print(self._obj.index)
        # print(self._obj.head())

    # @property
    def stationality(self, series):
        """Print out the stationality of the given series. Use multiple methods/test."""

        # TODO: Try/Catch for string or something?
        print("Stationality of {0}".format(series))

        values = self._obj[series].values

        # ADF
        # Bad unpack, also lots linting errors?
        # https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.adfuller.html
        result = {}
        adf_result = adfuller(values)

        result['adf'] = adf_result[0]
        result['pvalue'] = adf_result[1]
        result['usedlag'] = adf_result[2]
        result['nobs'] = adf_result[3]
        result['values'] = adf_result[4]
        result['icbest'] = adf_result[5]
        if len(adf_result) > 6:
            result['resstore'] = adf_result[6]  # Optional

        print('ADF Statistic: %f' % result['adf'])
        print('p-value: %f' % result['pvalue'])
        print('Critical Values:')
        for key, value in result['values'].items():
            print('\t%s: %.3f' % (key, value))
        print()

        # print('ADF Statistic: %f' % adf_result[0])
        # print('p-value: %f' % adf_result[1])
        # print('Critical Values:')
        # for key, value in adf_result[4].items():
        #     print('\t%s: %.3f' % (key, value))
        # print()

        # KPSS
        # kpss_result = kpss_test(values)

        return result





