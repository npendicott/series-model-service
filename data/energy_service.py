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
            lables = lables[1:]  # Grab index label
            values = result_series['values']
            data = [value[1:] for value in values]  # Drop index label

            timestamps = [value[0] for value in values]

            return table, timestamps, lables, data

        # Requests
        def get_readings(self, series, mac_id, start_date, end_date):
            headers = {'mac-id': mac_id}
            query = {'start': start_date,
                     'end': end_date}

            req_url = '{0}/readings/{1}'.format(self.ENERGY_URL, series)
            res = requests.get(req_url.format(), headers=headers, params=query)

            return self.parse_response(res)
