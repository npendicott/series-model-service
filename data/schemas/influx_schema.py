#  https://hynek.me/articles/serialization/
from marshmallow import Schema, fields, post_load, pprint
# TODO: Toast:
#  https://eng.lyft.com/toasted-marshmallow-marshmallow-but-15x-faster-17bdcf34c760


# London
class DailyReadingSchema(Schema):
    energy_count = fields.Int()
    energy_max = fields.Decimal()
    energy_mean = fields.Decimal()
    energy_median = fields.Decimal()
    energy_min = fields.Decimal()
    energy_std = fields.Decimal()
    energy_sum = fields.Decimal()
    mac_id = fields.Str()


class HHourlyReadingSchema(Schema):
    energy_median = fields.Decimal()
    mac_id = fields.Str()


# Solar
class SolarControlSchema(Schema):
    current = fields.Decimal()
    power = fields.Decimal()
    volt_al = fields.Decimal()
    volt_ce = fields.Decimal()


class SolarPandOSchema(Schema):
    current = fields.Decimal()
    current_adj = fields.Decimal()
    power = fields.Decimal()
    power_adj = fields.Decimal()
    volt_ce = fields.Decimal()
    volt_ce_adj = fields.Decimal()
    volt_sp = fields.Decimal()
    volt_sp_adj = fields.Decimal()


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
