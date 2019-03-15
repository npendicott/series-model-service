import numpy as np
# import pandas
from pandas import Series
from datetime import datetime
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose

from model.ryo_analysis import kpss_test, quick_autocorr

# The following works for the dang jupyter, should just keep everything in a flat dir I guess
# from app.ts_decomposition.model.ryo_analysis import kpss_test, quick_autocorr


# TODO: Inherit from df, so df calls go to base?
class TimeSeriesSample:
    """An object for holding time series data, for the purpose of data analysis and modeling."""

    # Base Dataframe
    # TODO: How do we deal with 'split' stuff? 'base' will be full until the split, then will only be
    #  the train set. 'base_valid' will be only be the validation set. Any transform over the full set will need to
    #  operate over the full set, but will also need to preserve the original split.
    #  possibility: with some decorator, merge the sets and save the split index, then re-split. Could just save the
    #  percent, but that seems less precise?
    base = None
    base_valid = None

    index = None  # Index of the sample, should probably be a time index
    train_test_split_index = None
    categorical_features = None

    # TODO: If index_key is None, check the actual frame index?
    def __init__(self, base, index_key=None, date_fmt_str="%Y-%m-%d %H:%M:%S", categorical_features=None):
        """
        Initialize the Sample from a base
        index_key: if it is filled in, will take the corrispodong series as index. parses with the date_fmt_str
        and datetime.strptime function.

        categorical_features: non-continuous features
        """

        self.base = base  # TODO: DataFrame, or NumPy Array?

        if base.index is None:
            raise TypeError("Dataframe needs an index!")

        if not isinstance(base.index[0], datetime):
                raise TypeError("Index must be datetime")
        # May need to raise this
        # except IndexError:
        #     raise IndexError("Index series as nothing at [0]!")


        # OLD
        # At first, I tried to parse in constructor. Now I am just checking
        # Set the index
        # if index_key is not None:
        #     try:
        #         index_series = self.base[index_key]
        #     except KeyError:
        #         raise KeyError("Index \"{0}\" not found!".format(index_key))
        #
        #     self.base.set_index(index_series, inplace=True) # TODO: Do we drop the "index" series?
        #
        # # Datetime Check
        # if not isinstance(self.base.index[0], datetime):
        #     try:
        #         # index_series = self.base.index.apply(lambda x: datetime.strptime(x, date_fmt_str))  # Apply
        #         new_index = [datetime.strptime(dt, date_fmt_str) for dt in self.base.index]
        #         self.base.set_index(new_index)
        #         # TODO: KeyError: datetime.datetime(2012, 4, 13, 0, 0)
        #
        #     except TypeError:
        #         raise TypeError("Cannot parse datetime index at \"{0}\".".format(index_key))
        #     except IndexError:
        #         raise IndexError("Index series as nothing at [0]!")
        #
        #     self.base.set_index(index_series, inplace=True) # TODO: Do we drop the "index" series?
        #

        # # TODO: Right now, features are either "categorical" or not. What other classifications are needed?
        if categorical_features is not None:
            self.categorical_features = categorical_features

    # Train/Test/Validation Split
    def train_test_split(self, valid_percent):
        """
        Splits off last valid_percent of the data to a validation set. Percent will come from last index of the
        array.
        """

        if self.base_valid is not None:
            pass  # TODO: Check for percent/base_valid? then rejoin?

        # Base
        if self.base is not None:
            self.base, self.base_valid = self._split_frame(self.base, valid_percent)

    @staticmethod
    def _split_frame(frame, percent):
        size = len(frame.index)

        if percent >= 100 or percent <= 0:
            raise ValueError("{0} is not a valid percent for train/test split")

        # TODO: Decimal check, or range check?
        #  i.e. will a valid set ever be half a percent? And is it cool to do type checks?
        if percent > 1:
            factor = (100 - percent) / 100
        else:
            factor = (1 - percent) / 100

        split_index = int(size * factor)
        train, validate = frame[0:split_index], frame[split_index:]

        return train, validate

    # TODO: Decorators: Apply on full set vs train/test, apply on quantitative/vs cat/qual
    # Decorator funcs?? For splitting and rejoining, if necessary.
    # def _rejoin(self):
    #     self.train_test_split_index = len(self.base)
    #     self.base = self.base + self.base_valid
    #
    # def _resplit(self):
    #     self.base, self.base_valid = self.base[:self.train_test_split_index], self.base[self.train_test_split_index:]
    #
    # # TODO: Want to make a wrapper that applies new features, or feature transforms, over BOTH train and test
    # @staticmethod
    # def across_splits(func):
    #     # TODO: @functools.wraps(func)
    #     def wrapper(*args, **kwargs):
    #         # self._rejoin()
    #
    #         func()
    #
    #         # self._resplit()
    #
    #     return wrapper
    #
    # @across_splits
    # def test_wrap_unwrap(self):
    #     print("base: {0}", len(self.base))
    #     print("base_valid: {0}", len(self.base_valid))

    # Creature Features
    def day_of_week_class(self):
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

        # Just need datetime.weekday for #
        # self.base['day_of_week_class'] = self.base[self.index].apply(datetime.weekday)

        self.base['day_of_week_class'] = [datetime.weekday(ts) for ts in self.base.index.values]


    def weekend_weekday_class(self):
        """Generate class for weekend_weekday_class. 0 is weekday."""

        def weekend_weekday(date):
            if date.weekday() == 5 or date.weekday() == 6:
                return 1
            else:
                return 0

        self.base['weekend_weekday_class'] = self.base[self.index].apply(weekend_weekday)

        # Clean

    def clean_lights(self, floor=0):
        """
        Add a light_on series to dataframe, indicating the lights were taking power. Add a light_cleaned with all
        zero light power values removed.
        """
        light_on_list = []
        light_cleaned_list = []

        for light_reading in self.base['light']:
            # Maybe some vals around 0?
            light_on = light_reading > floor

            if light_on:
                light_on_list.append(1)
                light_cleaned_list.append(light_reading)

            else:
                light_on_list.append(0)
                light_cleaned_list.append(None)

        light_on_series = Series(light_on_list)
        self.base['light_on'] = light_on_series

        light_cleaned_series = Series(light_cleaned_list)
        self.base['light_cleaned'] = light_cleaned_series

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
    def stationality(self, series, verbose=True):
        """Print out the stationality of the given series. Use multiple methods/test."""

        # TODO: Try/Catch for string or something?
        if verbose:
            print("Stationality of {0}".format(series))

        values = self.base[series].values

        # ADF
        adf_result = adfuller(values)

        if verbose:
            print('ADF Statistic: %f' % adf_result[0])
            print('p-value: %f' % adf_result[1])
            print('Critical Values:')
            for key, value in adf_result[4].items():
                print('\t%s: %.3f' % (key, value))
            print()

        # KPSS
        # kpss_result = kpss_test(values)

        # Combine results
        result = adf_result

        return result

    def autocorrelation(self, series, verbose=True):
        """
        Check the degree of autocorrelation of the given series.
        """

        if verbose:
            print("Autocorrelation of {0}".format(series))

        values = self.base[series].values

        result = quick_autocorr(values)

        if verbose:
            print("Quick:")
            print(result)
            print()

        # TODO: Autocorr stepdown/degree. Take autocorr of resid?

        return result

    # Decomposition
    # TODO: Centralize the decompose, with a fixed set of attributes to decompose to?
    #  or just seasonal_decompose wrapper?
    def decompose(self, series):
        # TODO: maybe decmpose-specific suffixes?
        period = 144  # Day
        # period = 1008 # Month

        two_side = True
        # two_side=False

        # model = 'additive'
        model = 'multiplicitive'

        result = seasonal_decompose(self.base[series].values, model=model, two_sided=two_side, freq=period)
        # # Cut off the NaNa on either side, from Moving Average loss
        # start_gap = period
        # end_gap = len(result.resid) - period

        # observed = result.observed[start_gap:end_gap]
        # residual = result.resid[start_gap:end_gap]

        # r_sqr = self.residual(observed, residual)

        # print(r_sqr)

        return result

    # ARIMA
    def generate_arima(self):
        pass

    # Util
    @staticmethod
    def calc_r_sqr(observed, residual):
        """Calculate the r_sqr from an observed set and residual set."""
        ss_res = sum([(e * e) for e in residual])

        y_bar = sum(observed) / len(observed)
        ss_tot = sum([((y - y_bar) * (y - y_bar)) for y in observed])

        r_sqr = 1 - (ss_res / ss_tot)

        return r_sqr

    # def print(self):
    #     # Base
    #     print("Base: ")
    #     print(self.base.describe())
    #     print(self.base.head())
    #     print(self.base.tail())
    #     print()
    #
    #     # Base Valid
    #     print("Base Validation: ")
    #     print(self.base_valid.describe())
    #     print(self.base_valid[self.index])
    #     print()
