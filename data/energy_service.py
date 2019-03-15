import requests
from pandas import DataFrame


class EnergyService:
        ENERGY_URL = 'http://192.168.0.24:9090'

        def __init__(self):
            pass

        def sample_data(self, mac_id, start_date, end_date):
            headers = {'mac-id': mac_id}
            query = {'start': start_date,
                     'end': end_date}

            # /readings/daily
            req_url = '{0}/readings/daily'.format(self.ENERGY_URL)
            res = requests.get(req_url.format(), headers=headers, params=query)

            res_json = res.json()

            result_series = res_json['Results'][0]['Series'][0]

            table = result_series['name']
            columns = result_series['columns']
            values = result_series['values']

            data = [value[1:] for value in values]
            index = [value[0] for value in values]

            # TODO: move this over hereeeeee
            # if index_key is not None:
            #     try:
            #         index_series = self.base[index_key]
            #     except KeyError:
            #         raise KeyError("Index \"{0}\" not found!".format(index_key))
            #
            #     self.base.set_index(index_series, inplace=True)  # TODO: Do we drop the "index" series?
            #
            # # Datetime Check
            # if not isinstance(self.base.index[0], datetime):
            #     try:
            #         # index_series = self.base.index.apply(lambda x: datetime.strptime(x, date_fmt_str))  # Apply
            #         new_index = [datetime.strptime(dt, date_fmt_str) for dt in self.base.index]
            #         self.base.set_index(new_index, inplace=True)
            #         # TODO: KeyError: datetime.datetime(2012, 4, 13, 0, 0)
            #
            #     except TypeError:
            #         raise TypeError("Cannot parse datetime index at \"{0}\".".format(index_key))
            #     except IndexError:
            #         raise IndexError("Index series as nothing at [0]!")
            #
            #     self.base.set_index(index_series, inplace=True)  # TODO: Do we drop the "index" series?

            frame = DataFrame(data=data, index= index, columns=columns[1:])

            return frame


if __name__ == "__main__":

    service = EnergyService()
    res = service.sample_data('MAC000246', '2012-04-12 10:30:00.0000000', '2012-07-12 10:30:00.0000000')

    print(res.head())

