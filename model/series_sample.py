from pandas import DataFrame, Series, Timestamp, DatetimeIndex, MultiIndex, RangeIndex
from pandas.api.extensions import register_dataframe_accessor

from statsmodels.tsa.stattools import adfuller

from model.ryo_analysis import kpss_test, quick_autocorr

# import numpy as np
# from pandas import Series, DataFrame, DatetimeIndex
# from datetime import datetime
# from statsmodels.tsa.stattools import adfuller
# from statsmodels.tsa.seasonal import seasonal_decompose
#
# from model.ryo_analysis import kpss_test, quick_autocorr


@register_dataframe_accessor("tss")
class TimeSeriesSampleAccessor:
    """ Adding accessor for some common time series modeling tasks to pandas DataFrame.

    http://pandas.pydata.org/pandas-docs/stable/development/extending.html#extending-subclassing-pandas
    http://pandas.pydata.org/pandas-docs/stable/development/extending.html#extending-register-accessors

    This is a good example apparently: https://github.com/geopandas/geopandas/blob/master/geopandas/geodataframe.py
    """

    # CREATE/CHECK DataFrame
    def __init__(self, pandas_obj):
        # self._validate(pandas_obj)
        self._obj = pandas_obj

    # TODO: Update, also figure out when it needs to enter the picture
    @staticmethod
    def _validate(obj):
        if not isinstance(obj.index, DatetimeIndex):
            if 'timestamp' not in obj.columns:
                raise TypeError("Index must be correctly formatted or contain a 'timestamp' column.")

    # Extended methods
    def format_index(self, index, time_fmt):
        """Sets the index."""
        datetime_index_key = 'timestamp'  # TODO: Some object for 'model_keys'

        if isinstance(index[0], Timestamp):
            index = [Timestamp.strptime(ts, time_fmt) for ts in self._obj[datetime_index_key]]
        timestamp_index = DatetimeIndex(index)
        self._obj.set_index(timestamp_index, inplace=True)

    # Diagnostics
    # Could use @property and a cache in the object to save time, if repeated calls across
    # different series slow things down.
    def stationality(self, series):
        """Print out the stationality of the given series. Use multiple methods/test."""

        # TODO: Try/Catch for string or something?
        print("Stationality of {0}".format(series))

        values = self._obj[series]
        if isinstance(values[0], str):
            values = Series([float(val) for val in values])
            # TODO: Sometimes stuff comes out of this pd as str, don't want to manualy cast

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
        if len(adf_result) > 6:  # how to do this on dict init?
            result['resstore'] = adf_result[6]  # Optional

        # print('ADF Statistic: %f' % result['adf'])
        # print('p-value: %f' % result['pvalue'])
        # print('Critical Values:')
        # for key, value in result['values'].items():
        #     print('\t%s: %.3f' % (key, value))
        # print()

        # print('ADF Statistic: %f' % adf_result[0])
        # print('p-value: %f' % adf_result[1])
        # print('Critical Values:')
        # for key, value in adf_result[4].items():
        #     print('\t%s: %.3f' % (key, value))
        # print()

        # KPSS
        # kpss_result = kpss_test(values)

        return result

    def autocorrelation(self, series):
        """
        Check the degree of autocorrelation of the given series.
        """

        values = self._obj[series].values
        if isinstance(values[0], str):
            values = Series([float(val) for val in values])
            # TODO: Sometimes stuff comes out of this pd as str, don't want to manualy cast, same as above


        result = quick_autocorr(values)

        # print("Autocorrelation of {0}".format(series))
        #
        # print("Quick:")
        # print(result)
        # print()

        # TODO: Autocorr stepdown/degree. Take autocorr of resid?

        return result

    # Creature Features
    def day_of_week_class(self, inplace=True):
        """Add series to dataframe for a day_of_week_class classification."""
        # # This func is for labels if needed
        # def get_day(date):
        #     day_int = date.weekday()

        #     day_switch = {
        #         0: "Monday",
        #         1: "Tuesday",
        #         2: "Wednesday",
        #         3: "Thursday",
        #         4: "Friday",
        #         5: "Saturday",
        #         6: "Sunday"
        #     }
        #     return day_switch.get(day_int, "Invalid day")

        # frame = self._obj
        # index = frame.index
        # sub_frame = frame[:5]
        # print(len(sub_frame))
        day_of_week_class = [ts.weekday() for ts in self._obj.index]

        # self.append(())
        # dows = Series(data=[datetime.weekday(ts) for ts in self.datetime_index], name='day_of_week_class')
        # self.append(dows)
        # self.['day_of_week_class_label'] = [datetime.weekday(ts) for ts in self..values]

        return day_of_week_class

    # def weekend_weekday_class(self):
    #     """Generate class for weekend_weekday_class. 0 is weekday."""
    #
    #     def weekend_weekday(date):
    #         if date.weekday() == 5 or date.weekday() == 6:
    #             return 1
    #         else:
    #             return 0
    #
    #     self.base['weekend_weekday_class'] = self.base[self.index].apply(weekend_weekday)
    #
    #     # Clean
    #
    # def clean_lights(self, floor=0):
    #     """
    #     Add a light_on series to dataframe, indicating the lights were taking power. Add a light_cleaned with all
    #     zero light power values removed.
    #     """
    #     light_on_list = []
    #     light_cleaned_list = []
    #
    #     for light_reading in self.base['light']:
    #         # Maybe some vals around 0?
    #         light_on = light_reading > floor
    #
    #         if light_on:
    #             light_on_list.append(1)
    #             light_cleaned_list.append(light_reading)
    #
    #         else:
    #             light_on_list.append(0)
    #             light_cleaned_list.append(None)
    #
    #     light_on_series = Series(light_on_list)
    #     self.base['light_on'] = light_on_series
    #
    #     light_cleaned_series = Series(light_cleaned_list)
    #     self.base['light_cleaned'] = light_cleaned_series

    # Graphing
    # TODO: Want to start putting some methods to genreate plot items?
    # From hist, return: axes: matplotlib.AxesSubplot or numpy.ndarray of them
    # def plot_series_features(self):
    #
    #     series_plots = []
    #     for series in self.base:
    #         if series not in self.categorical_features:
    #             series_plots.append(self.base.plot(kind='line', x=self.base.index, y=series))
    #
    #     return series_plots
    #     pass
    #
    # def plot_categorical_features(self):
    #     series_plots = []
    #
    #     for series in self.base:
    #         if series in self.categorical_features:
    #             series_plots.append(self.base.plot(kind='line', x=self.base.index, y=series))
    #
    #     return series_plots

    # Diagnostics







