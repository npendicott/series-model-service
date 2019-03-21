import numpy as np
# import pandas
from pandas import Series, DataFrame, DatetimeIndex
from datetime import datetime
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose

from model.ryo_analysis import kpss_test, quick_autocorr

# The following works for the dang jupyter, should just keep everything in a flat dir I guess
# from app.ts_decomposition.model.ryo_analysis import kpss_test, quick_autocorr


# TODO: Inherit from df, so df calls go to base?
class TimeSeriesModel:
    """ This object will hold various time series models, such as ARIMA models or an LSTM model.
    Will include serialization/export methods, and tests, etc.

    Right now it is old stuff, in the process of stripping and reworking.
    """

    # normal properties
    _metadata = [
        'datetime_index',
        # 'dt_index',

        'categorical_features',
        'validation_split_index',
        'validation_set',
    ]

    datetime_index = None

    categorical_features = None
    validation_split_index = None
    validation_set = None


    # base = None
    # base_valid = None
    #
    # index = None  # Index of the sample, should probably be a time index
    # train_test_split_index = None
    # categorical_features = None

    # TODO: If index_key is None, check the actual frame index?
    def __init__(self, *args, **kwargs): #data, index=None, categorical_features=None):
        """
        Initialize the sample dataframe, check for proper indexing.
        Will also do a validation split, if valid_percent is provided
        """
        # TODO: TEST Doesnt throw arg error
        # Unpack RYO Args
        categorical_features = kwargs.pop('categorical_features', None)
        valid_percent = kwargs.pop('valid_percent', None)  # TODO: Impliment
        datetime_index = kwargs.pop('datetime_index', None)


        # IMPORTANT: So here, we are pretty much creating two indices, a datetime and an int range.
        # Pandas has some support for multiple indices, but the whole [0][1] is not my fave.
        # So, I guess the choice here is: do we maintain multiple indices??
        # TODO: DatetimeIndex Throwing freq error
        # TODO: Sometimes, valid percent line 172 drops us in the constructor, and we are looking for a dti
        if datetime_index is not None:
            self.datetime_index = datetime_index
            self.datetime_index = [datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ") for dt in datetime_index]

            # for dt in datetime_index:
            #     datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")

            # for dt in datetime_index:
            #     datetime.strftime()

            # self.datetime_index = Series(datetime_index)
            # if isinstance(self.datetime_index[0], datetime):
            #     print("it is")
            # self.datetime_index_index = None

        self.categorical_features = categorical_features

        # Sooo... everything before or after super? Mixx? -> what can be before, should be before, reduce deps
        super(TimeSeriesSample, self).__init__(*args, **kwargs)

        if valid_percent is not None:
            self.valid_split(valid_percent)

        # Checks
        # TODO: Easier to just check the super, but validating args will cause more efficient faulure
        # if data.index is None and index is None:
        #     raise TypeError("Dataframe needs an index!")
        #
        # if not isinstance(base.index[0], datetime):
        #         raise TypeError("Index must be datetime")
        #
        # # # TODO: Right now, features are either "categorical" or not. What other classifications are needed?
        # if categorical_features is not None:
        #     self.categorical_features = categorical_features
        # if not isinstance(base.index[0], datetime):
        #         raise TypeError("Index must be datetime")
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


    def valid_split(self, percent):
        """
        Splits off last valid_percent of the data to a validation set. Percent will come from last index of the
        array.
        """

        if self.validation_set is not None:
            pass  # TODO: Check for percent/base_valid? then rejoin?

        size = len(self.index)

        if percent >= 100 or percent <= 0:
            raise ValueError("{0} is not a valid percent for train/test split")

        # TODO: Decimal check, or range check?
        #  i.e. will a valid set ever be half a percent? And is it cool to do type checks?
        if percent > 1:
            factor = (100 - percent) / 100
        else:
            factor = (1 - percent) / 100

        split_index = int(size * factor)

        self.validation_split_index = split_index
        self.validation_set = self[split_index:]

        drop_array = [i for i in range(split_index, size)]  # Debug, maybe remove
        # drop_array = [self[i] for i in range(split_index, size)]

        self.drop(drop_array, inplace=True)
        # self.drop([i for i in range(split_index, size)], inplace=True)

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

    def print(self):
        print(self.tail())
        print("Length: {0}".format(len(self)))
        # print(self.train_test_split_index)
        print("Categorical Features: {0}".format(self.categorical_features))
