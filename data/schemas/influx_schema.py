#  https://hynek.me/articles/serialization/
from marshmallow import Schema, fields, post_load, pprint
# TODO: Toast:
#  https://eng.lyft.com/toasted-marshmallow-marshmallow-but-15x-faster-17bdcf34c760


# London
class DailyReadingSchema(Schema):
    energy_count = fields.Int()
    energy_max = fields.Float()
    energy_mean = fields.Float()
    energy_median = fields.Float()
    energy_min = fields.Float()
    energy_std = fields.Float()
    energy_sum = fields.Float()
    mac_id = fields.Str()


class HHourlyReadingSchema(Schema):
    energy_median = fields.Float()
    mac_id = fields.Str()


# Solar
class SolarControlSchema(Schema):
    current = fields.Float()
    power = fields.Float()
    volt_al = fields.Float()
    volt_ce = fields.Float()


class SolarPandOSchema(Schema):
    current = fields.Float()
    current_adj = fields.Float()
    power = fields.Float()
    power_adj = fields.Float()
    volt_ce = fields.Float()
    volt_ce_adj = fields.Float()
    volt_sp = fields.Float()
    volt_sp_adj = fields.Float()


# class SolarControl(object):
#     def __init__(self):
#
#     "time",
#     "current",
#     "power",
#     "volt_al",
#     "volt_ce"
#




class ResponseSechema(Schema):
    results = fields.Dict(
        keys=fields.Str(),

    )
    def __init__(self, results):
        self.results = results


# TODO: I can pop these guys off and just format table types for now
# class Series(Schema):
#     name = fields.Str()
#     columns = [fields.Str()]
#     values = []
#
#
# class Result(Schema):
#     Series = [Series]
#     Messages = fields.Str()
#
#
#
#
# class ResponseS(Schema):
#     Results = [fields.Nested(Result)]
#
#     @post_load
#     def make_response(self, data):
#         return
