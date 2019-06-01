import requests
# from datetime import datetime


from pprint import pprint


class EnergyService:
    ENERGY_URL = 'http://localhost:9090'

    # ENERGY_URL = 'http://192.168.0.24:9090'
    # date_fmt_str = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self):
        pass

    # Schema
    # TODO: Parse to some output and then feed to a "Flatten" method??
    @staticmethod
    def parse_response(res, schema):
        res = res.json()  # TODO: Take a json, or response? What checks?
        try:
            result = res['Results'][0]
        except TypeError:
            raise TypeError("Result set is empty!")

        try:
            result_series = result['Series'][0]
        except TypeError:
            raise TypeError("Series is empty!")

        # schema = DailyReadingSchema()  # TODO: Inject this

        # Func validation
        def validate(reading):
            return schema.load({lables[i]: reading[i] for i in range(len(reading))}).data
            # return schema.dump(reading_struct).data

        # New
        table = result_series['name']
        lables = result_series['columns'][1:]  # drop index label

        timestamps = []
        data = []
        for value in result_series['values']:
            timestamps.append(value[0])
            data.append(validate((value[1:])))  # drop index val and validate

        # [pprint(record) for record in data]
        return table, timestamps, lables, data

    # Requests
    def get_readings(self, series, mac_id, start_date, end_date):
        headers = {'mac-id': mac_id}
        query = {'start': start_date,
                 'end': end_date}

        req_url = '{0}/readings/{1}'.format(self.ENERGY_URL, series)
        res = requests.get(req_url.format(), headers=headers, params=query)

        return res
