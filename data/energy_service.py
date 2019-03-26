import requests
#from pandas import DataFrame
# from datetime import datetime


class EnergyService:
        # ENERGY_URL = 'http://192.168.0.24:9090'
        ENERGY_URL = 'http://localhost:9090'

        date_fmt_str = "%Y-%m-%dT%H:%M:%SZ"

        def __init__(self):
            pass

        # Schema
        @staticmethod
        def parse_response(res):
            res = res.json()  # TODO: Take a json, or response? What checks?

            # Unpack Result/Series
            try:
                result = res['Results'][0]
            except TypeError:
                raise TypeError("Result set is empty!")

            try:
                result_series = result['Series'][0]
            except TypeError:
                raise TypeError("Series is empty!")

            # Format into output objects
            table = result_series['name']

            lables = result_series['columns']
            lables = lables[1:]  # Drop index label

            values = result_series['values']
            data = [value[1:] for value in values]  # Drop index lables

            timestamps = [value[0] for value in values]

            return table, timestamps, lables, data

        # Requests
        def daily_reading(self, mac_id, start_date, end_date):

            headers = {'mac-id': mac_id}
            query = {'start': start_date,
                     'end': end_date}

            req_url = '{0}/readings/daily'.format(self.ENERGY_URL)
            res = requests.get(req_url.format(), headers=headers, params=query)

            return self.parse_response(res)

        def hhourly_reading(self, mac_id, start_date, end_date):
            pass

        # OLD
        # def sample_data(self, mac_id, start_date, end_date):
        #     """Samples time series data. Returns a Pandas dataframe"""
        #
        #     headers = {'mac-id': mac_id}
        #     query = {'start': start_date,
        #              'end': end_date}
        #
        #     req_url = '{0}/readings/daily'.format(self.ENERGY_URL)
        #     res = requests.get(req_url.format(), headers=headers, params=query)
        #     res_json = res.json()
        #
        #     try:
        #         result = res_json['Results'][0]
        #     except TypeError:
        #         raise TypeError("Result set is empty!")
        #
        #     try:
        #         result_series = result['Series'][0]
        #     except TypeError:
        #         raise TypeError("Series is empty!")
        #
        #
        #
        #     # try:
        #     #     result_series = res_json['Results'][0]['Series'][0]
        #     # except None
        #
        #
        #
        #     table = result_series['name']
        #
        #     columns = result_series['columns']
        #     columns = columns[1:]  # Drop index label
        #
        #     values = result_series['values']
        #     data = [value[1:] for value in values]
        #     timestamps = [value[0] for value in values]
        #
        #     # Datetime Check
        #     # if not isinstance(index[0], datetime):
        #     #     try:
        #     #         # index_series = self.base.index.apply(lambda x: datetime.strptime(x, date_fmt_str))  # Apply
        #     #         index = [datetime.strptime(dt, self.date_fmt_str) for dt in index]
        #     #
        #     #     except TypeError:
        #     #         raise TypeError("Cannot parse datetime: \"{0}\".".format(index[0]))
        #     #     except IndexError:
        #     #         raise IndexError("Index series as nothing at [0]!")
        #
        #         # self.base.set_index(index_series, inplace=True)  # TODO: Do we drop the "index" series?
        #
        #     return table, timestamps, columns, data
        #
        #     # frame = DataFrame(data=data, index=index, columns=columns[1:])
        #     # frame = DataFrame(data=data)#, #index=index, columns=columns[1:])
        #     #
        #     # print(frame.head())
        #     # return frame
        #

# if __name__ == "__main__":
#
#     service = EnergyService()
#     res = service.sample_data('MAC000246', '2012-04-12 10:30:00.0000000', '2012-07-12 10:30:00.0000000')
#
#     print(res.head())

