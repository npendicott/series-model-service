import requests
#from pandas import DataFrame
from datetime import datetime


class EnergyService:
        ENERGY_URL = 'http://192.168.0.24:9090'

        date_fmt_str = "%Y-%m-%dT%H:%M:%SZ"

        def __init__(self):
            pass

        def sample_data(self, mac_id, start_date, end_date):
            """Samples time series data. Returns a Pandas dataframe"""

            headers = {'mac-id': mac_id}
            query = {'start': start_date,
                     'end': end_date}

            req_url = '{0}/readings/daily'.format(self.ENERGY_URL)
            res = requests.get(req_url.format(), headers=headers, params=query)
            res_json = res.json()

            result_series = res_json['Results'][0]['Series'][0]

            table = result_series['name']

            columns = result_series['columns']
            columns = columns[1:]  # Drop index label

            values = result_series['values']
            data = [value[1:] for value in values]
            index = [value[0] for value in values]

            # Datetime Check
            if not isinstance(index[0], datetime):
                try:
                    # index_series = self.base.index.apply(lambda x: datetime.strptime(x, date_fmt_str))  # Apply
                    index = [datetime.strptime(dt, self.date_fmt_str) for dt in index]

                except TypeError:
                    raise TypeError("Cannot parse datetime: \"{0}\".".format(index[0]))
                except IndexError:
                    raise IndexError("Index series as nothing at [0]!")

                # self.base.set_index(index_series, inplace=True)  # TODO: Do we drop the "index" series?

            return table, columns, index, data

            # frame = DataFrame(data=data, index=index, columns=columns[1:])
            frame = DataFrame(data=data)#, #index=index, columns=columns[1:])

            print(frame.head())
            return frame


# if __name__ == "__main__":
#
#     service = EnergyService()
#     res = service.sample_data('MAC000246', '2012-04-12 10:30:00.0000000', '2012-07-12 10:30:00.0000000')
#
#     print(res.head())

