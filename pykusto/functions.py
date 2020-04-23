import json
from typing import Union

from pykusto.expressions import AnyTypeColumn, NumberType, NumberExpression, TimespanType, \
    DatetimeExpression, TimespanExpression, ArrayType, DynamicType, DatetimeType, BaseExpression, BooleanType, \
    ExpressionType, AggregationExpression, StringType, StringExpression, BooleanExpression, \
    NumberAggregationExpression, MappingAggregationExpression, ArrayAggregationExpression, to_kql, DynamicExpression, \
    ArrayExpression, ColumnToType, BaseColumn, AnyExpression, AnyAggregationExpression, MappingExpression
from pykusto.kql_converters import KQL
from pykusto.logger import logger
from pykusto.type_utils import plain_expression, KustoType


class Functions:
    """
    Recommended import style:\n
    `from pykusto.functions import Functions as f`
    """
    # Scalar functions

    @staticmethod
    def acos(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/acosfunction
        """
        return expr.acos()

    @staticmethod
    def ago(expr: TimespanType) -> DatetimeExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/agofunction
        """
        return TimespanExpression.ago(expr)

    # def array_concat(): return
    #
    #
    # def array_iif(): return

    @staticmethod
    def array_length(expr: ArrayType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/arraylengthfunction
        """
        return ArrayExpression(expr).array_length()

    # def array_slice(): return
    #
    #
    # def array_split(): return
    #
    #
    # def asin(): return
    #
    #
    # def atan(self): return
    #
    #
    # def atan2(self): return
    #
    #
    # def base64_decode_toarray(self): return
    #
    #
    # def base64_decode_tostring(self): return
    #
    #
    # def base64_encode_tostring(self): return
    #
    #
    @staticmethod
    def bag_keys(expr: DynamicType):
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/bagkeysfunction
        """
        return expr.keys()

    # def beta_cdf(self): return
    #
    #
    # def beta_inv(self): return
    #
    #
    # def beta_pdf(self): return

    @staticmethod
    def bin(expr: Union[NumberType, DatetimeType, TimespanType],
            round_to: Union[NumberType, TimespanType]) -> BaseExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/binfunction\n
        Refers only to bin() as part of summarize by bin(...),
         if you wish to use it as a scalar function, use 'floor()' instead
        :param expr: A number, date, or timespan.
        :param round_to: The "bin size". A number, date or timespan that divides value.
        :return:
        """
        return expr.bin(round_to)

    @staticmethod
    def bin_at(expr: Union[NumberType, DatetimeType, TimespanType],
               bin_size: Union[NumberType, TimespanType],
               fixed_point: Union[NumberType, DatetimeType, TimespanType]) -> BaseExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/binatfunction
        """
        return expr.bin_at(bin_size, fixed_point)

    @staticmethod
    def bin_auto(expr: Union[NumberType, DatetimeType, TimespanType]) -> BaseExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/bin-autofunction
        """
        return expr.bin_auto()

    # def binary_and(self): return
    #
    #
    # def binary_not(self): return
    #
    #
    # def binary_or(self): return
    #
    #
    # def binary_shift_left(self): return
    #
    #
    # def binary_shift_right(self): return
    #
    #
    # def binary_xor(self): return

    @staticmethod
    def case(predicate: BooleanType, val: ExpressionType, *args: Union[BooleanType, ExpressionType]) -> AnyExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/casefunction
        """
        res = 'case({}, {}, {})'.format(
            to_kql(predicate), to_kql(val), ', '.join([to_kql(arg) for arg in args])
        )
        return AnyExpression(KQL(res))

    @staticmethod
    def ceiling(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/ceilingfunction
        """
        return expr.ceiling()

    # def coalesce(self): return
    #
    #
    # def column_ifexists(self): return
    #
    #

    @staticmethod
    def cos(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/cosfunction
        """
        return expr.cos()

    # def cot(self): return

    # def countof(self): return
    #
    #
    # def current_cluster_endpoint(self): return
    #
    #
    # def current_cursor(self): return
    #
    #
    # def current_database(self): return
    #
    #
    # def current_principal(self): return
    #
    #
    # def cursor_after(self): return
    #
    #
    # def cursor_before_or_at(self): return
    #
    #
    # def cursor_current(self): return
    #
    # def datetime_add(self): return
    #
    #
    # def datetime_part(self): return
    #
    #
    # def datetime_diff(self): return
    #
    #
    # def dayofmonth(self): return
    #
    #
    # def dayofweek(self): return
    #
    #
    # def dayofyear(self): return

    # def dcount_hll(expr: ExpressionType) -> BaseExpression:
    #     return BaseExpression(KQL('dcount_hll({})'.format(to_kql(expr))))

    # def degrees(self): return

    @staticmethod
    def end_of_day(expr: DatetimeExpression, offset: NumberType = None) -> DatetimeExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/endofdayfunction
        """
        return expr.end_of_day(offset)

    @staticmethod
    def end_of_month(expr: DatetimeType, offset: NumberType = None) -> DatetimeExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/endofmonthfunction
        """
        return expr.end_of_month(offset)

    @staticmethod
    def end_of_week(expr: DatetimeType, offset: NumberType = None) -> DatetimeExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/endofweekfunction
        """
        return expr.end_of_week(offset)

    @staticmethod
    def end_of_year(expr: DatetimeType, offset: NumberType = None) -> DatetimeExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/endofyearfunction
        """
        return expr.end_of_year(offset)

    # def estimate_data_size(self): return

    @staticmethod
    def exp(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/exp-function
        """
        return expr.exp()

    @staticmethod
    def exp10(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/exp10-function
        """
        return expr.exp10()

    @staticmethod
    def exp2(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/exp2-function
        """
        return expr.exp2()

    # def extent_id(self): return
    #
    #
    # def extent_tags(self): return
    #
    #
    # def extract(self): return
    #
    #
    # def extract_all(self): return
    #
    #
    # def extractjson(self): return

    @staticmethod
    def floor(expr: Union[NumberType, DatetimeType],
              round_to: Union[NumberType, TimespanType]) -> Union[NumberExpression, DatetimeExpression]:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/floorfunction
        """
        return expr.floor(round_to)

    @staticmethod
    def format_datetime(expr: DatetimeExpression, format_string: StringType) -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/format-datetimefunction
        """
        return expr.format_datetime(format_string)

    @staticmethod
    def format_timespan(expr: TimespanType, format_string: StringType) -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/format-timespanfunction
        """
        return expr.format_timespan(format_string)

    # def gamma(self): return

    @staticmethod
    def get_month(expr: DatetimeType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/getmonthfunction
        """
        return expr.get_month()

    @staticmethod
    def get_type(expr: ExpressionType) -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/gettypefunction
        """
        return expr.get_type()

    @staticmethod
    def get_year(expr: DatetimeType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/getyearfunction
        """
        return expr.get_year()

    @staticmethod
    def hash(expr: ExpressionType) -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/hashfunction
        """
        return expr.__hash__()

    @staticmethod
    def hash_sha256(expr: ExpressionType) -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/sha256hashfunction
        """
        return expr.hash_sha256()

    @staticmethod
    def hour_of_day(expr: DatetimeType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/hourofdayfunction
        """
        return expr.hour_of_day()

    @staticmethod
    def iff(predicate: BooleanType, if_true: ExpressionType, if_false: ExpressionType) -> BaseExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/ifffunction
        """
        return_types = plain_expression.get_base_types(if_true)
        other_types = plain_expression.get_base_types(if_false)
        common_types = other_types & return_types
        if len(common_types) == 0:
            # If there is not at least one common type, then certainly the arguments are not of the same type
            logger.warning(
                "The second and third arguments must be of the same type, but they are: {} and {}. "
                "If this is a mistake, please report it at https://github.com/Azure/pykusto/issues".format(
                    ", ".join(sorted(t.primary_name for t in return_types)),
                    ", ".join(sorted(t.primary_name for t in other_types))
                )
            )
            expression_type = AnyExpression
        else:
            expression_type = plain_expression.registry[next(iter(common_types))]
        return expression_type(
            KQL('iff({}, {}, {})'.format(to_kql(predicate), to_kql(if_true), to_kql(if_false)))
        )

    @staticmethod
    def iif(predicate: BooleanType, if_true: ExpressionType, if_false: ExpressionType) -> BaseExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/iiffunction
        """
        return Functions.iff(predicate, if_true, if_false)

    #
    # def indexof(self): return
    #
    #
    # def indexof_regex(self): return
    #
    #
    # def ingestion_time(self): return
    #
    #
    # def isascii(self): return

    @staticmethod
    def is_empty(expr: ExpressionType) -> BooleanExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/isemptyfunction
        """
        return expr.is_empty()

    @staticmethod
    def is_finite(expr: NumberType) -> BooleanExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/isfinitefunction
        """
        return expr.isfinite()

    @staticmethod
    def is_inf(expr: NumberType) -> BooleanExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/isinffunction
        """
        return expr.is_inf()

    @staticmethod
    def is_nan(expr: NumberExpression) -> BooleanExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/isnanfunction
        """
        return expr.is_nan()

    @staticmethod
    def is_not_empty(expr: ExpressionType) -> BooleanExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/isnotemptyfunction
        """
        return expr.is_not_empty()

    @staticmethod
    def is_not_null(expr: ExpressionType) -> BooleanExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/isnotnullfunction
        """
        return expr.is_not_null()

    @staticmethod
    def is_null(expr: ExpressionType) -> BooleanExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/isnullfunction
        """
        return expr.is_null()

    @staticmethod
    def is_utf8(expr: StringType) -> BooleanExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/isutf8
        """
        return expr.is_utf8()

    @staticmethod
    def log(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/log-function
        """
        return expr.log()

    @staticmethod
    def log10(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/log10-function
        """
        return expr.log10()

    @staticmethod
    def log2(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/log2-function
        """
        return expr.log2()

    @staticmethod
    def log_gamma(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/loggammafunction
        """
        return expr.log_gamma()

    @staticmethod
    def make_datetime(year: NumberType,
                      month: NumberType,
                      day: NumberType,
                      hour: NumberType = None,
                      minute: NumberType = None,
                      second: NumberType = None) -> DatetimeExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/make-datetimefunction
        """
        res = 'make_datetime({year}, {month}, {day}, {hour}, {minute}, {second})'.format(
            year=to_kql(year),
            month=to_kql(month),
            day=to_kql(day),
            hour=to_kql(0 if hour is None else hour),
            minute=to_kql(0 if minute is None else minute),
            second=to_kql(0 if second is None else second)
        )
        return DatetimeExpression(KQL(res))

    @staticmethod
    def make_string() -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/makestringfunction
        """
        raise NotImplemented  # pragma: no cover

    @staticmethod
    def make_timespan() -> TimespanExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/make-timespanfunction
        """
        raise NotImplemented  # pragma: no cover

    # def max_of(self): return
    #
    #
    # def min_of(self): return

    @staticmethod
    def month_of_year() -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/monthofyearfunction
        """
        raise NotImplemented  # pragma: no cover

    @staticmethod
    def new_guid() -> AnyExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/newguidfunction
        """
        raise NotImplemented  # pragma: no cover

    @staticmethod
    def now(offset: TimespanType = None) -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/nowfunction
        """
        if offset:
            return StringExpression(KQL('now({})'.format(to_kql(offset))))
        return StringExpression(KQL('now()'))

    @staticmethod
    def pack(**kwargs: ExpressionType) -> MappingExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/packfunction
        """
        return MappingExpression(KQL('pack({})'.format(
            ', '.join('"{}", {}'.format(k, to_kql(v)) for k, v in kwargs.items())
        )))

    @staticmethod
    def pack_all() -> MappingExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/packallfunction
        """
        raise NotImplemented  # pragma: no cover

    @staticmethod
    def pack_array(*elements: ExpressionType) -> 'ArrayExpression':
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/packarrayfunction
        """
        return ArrayExpression(KQL('pack_array({})'.format(
            ', '.join(to_kql(e) for e in elements)
        )))

    @staticmethod
    def pack_dictionary() -> MappingExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/packdictionaryfunction
        """
        raise NotImplemented  # pragma: no cover

    #
    #
    # def parse_csv(self): return
    #
    #
    # def parse_ipv4(self): return

    @staticmethod
    def parse_json(expr: Union[StringType, DynamicType]) -> DynamicExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/parsejsonfunction
        """
        return DynamicExpression(KQL('parse_json({})'.format(to_kql(expr))))

    # def parse_path(self): return
    #
    #
    # def parse_url(self): return
    #
    #
    # def parse_urlquery(self): return
    #
    #
    # def parse_user_agent(self): return
    #
    #
    # def parse_version(self): return
    #
    #
    # def parse_xml(self): return

    @staticmethod
    def percentile_tdigest() -> AnyExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/percentile-tdigestfunction
        """
        raise NotImplemented  # pragma: no cover

    @staticmethod
    def percentrank_tdigest() -> AnyExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/percentrank-tdigestfunction
        """
        raise NotImplemented  # pragma: no cover

    @staticmethod
    def pow(expr1: NumberType, expr2: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/powfunction
        """
        return NumberExpression(KQL('pow({}, {})'.format(to_kql(expr1), to_kql(expr2))))

    # def radians(self): return
    #
    #
    # def rand(self): return
    #
    #
    # def range(self): return
    #
    #
    # def rank_tdigest(self): return
    #
    #
    # def repeat(self): return

    # def replace(self): return

    # def reverse(self): return

    @staticmethod
    def round(expr: NumberType, precision: NumberType = None) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/roundfunction
        """
        return expr.round(precision)

    # def series_add(self): return
    #
    #
    # def series_decompose(self): return
    #
    #
    # def series_decompose_anomalies(self): return
    #
    #
    # def series_decompose_forecast(self): return
    #
    #
    # def series_divide(self): return
    #
    #
    # def series_equals(self): return
    #
    #
    # def series_fill_backward(self): return
    #
    #
    # def series_fill_const(self): return
    #
    #
    # def series_fill_forward(self): return
    #
    #
    # def series_fill_linear(self): return
    #
    #
    # def series_fir(self): return
    #
    #
    # def series_fit_2lines(self): return
    #
    #
    # def series_fit_2lines_dynamic(self): return
    #
    #
    # def series_fit_line(self): return
    #
    #
    # def series_fit_line_dynamic(self): return
    #
    #
    # def series_greater(self): return
    #
    #
    # def series_greater_equals(self): return
    #
    #
    # def series_iir(self): return
    #
    #
    # def series_less(self): return
    #
    #
    # def series_less_equals(self): return
    #
    #
    # def series_multiply(self): return
    #
    #
    # def series_not_equals(self): return
    #
    #
    # def series_outliers(self): return
    #
    #
    # def series_periods_detect(self): return
    #
    #
    # def series_periods_validate(self): return
    #
    #
    # def series_seasonal(self): return
    #
    #
    # def series_stats(self): return
    #
    #
    # def series_stats_dynamic(self): return
    #
    #
    # def series_subtract(self): return
    #
    #
    # def set_difference(self): return
    #
    #
    # def set_intersect(self): return
    #
    #
    # def set_union(self): return

    @staticmethod
    def sign(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/signfunction
        """
        return NumberExpression(KQL('sign({})'.format(to_kql(expr))))

    # def sin(self): return
    #
    #
    @staticmethod
    def split(string: StringType, delimiter: StringType, requested_index: NumberType = None) -> 'ArrayExpression':
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/splitfunction
        """
        return StringExpression(to_kql(string)).split(delimiter, requested_index)

    @staticmethod
    def sqrt(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/sqrtfunction
        """
        return NumberExpression(KQL('sqrt({})'.format(to_kql(expr))))

    @staticmethod
    def start_of_day(expr: DatetimeType, offset: NumberType = None) -> DatetimeExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/startofdayfunction
        """
        return expr.start_of_day(offset)

    @staticmethod
    def start_of_month(expr: DatetimeType, offset: NumberType = None) -> DatetimeExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/startofmonthfunction
        """
        return expr.start_of_month(offset)

    @staticmethod
    def start_of_week(expr: DatetimeType, offset: NumberType = None) -> DatetimeExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/startofweekfunction
        """
        return expr.start_of_week(offset)

    @staticmethod
    def start_of_year(expr: DatetimeType, offset: NumberType = None) -> DatetimeExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/startofyearfunction
        """
        return expr.start_of_year(offset)

    @staticmethod
    def strcat(*strings: StringType) -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/strcatfunction
        """
        if len(strings) < 2:
            raise ValueError("strcat requires at least two arguments")
        return StringExpression(KQL('strcat({})'.format(', '.join(to_kql(s) for s in strings))))

    @staticmethod
    def to_literal_dynamic(d: DynamicType) -> KQL:
        if isinstance(d, BaseExpression):
            return d.kql
        return KQL('dynamic({})'.format(json.dumps(d)))

    @staticmethod
    def strcat_array(expr: ArrayType, delimiter: StringType) -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/strcat-arrayfunction
        """
        return StringExpression(KQL('strcat_array({}, {})'.format(Functions.to_literal_dynamic(expr), to_kql(delimiter))))

    @staticmethod
    def strcat_delim(delimiter: StringType, expr1: StringType, expr2: StringType, *expressions: StringType) -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/strcat-delimfunction
        """
        res = 'strcat_delim({}, {}, {}'.format(
            to_kql(delimiter),
            to_kql(expr1),
            to_kql(expr2))
        if len(expressions) > 0:
            res = res + ', ' + ', '.join([to_kql(expr) for expr in expressions])
        return StringExpression(KQL(res + ')'))

    @staticmethod
    def strcmp(expr1: StringType, expr2: StringType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/strcmpfunction
        """
        return NumberExpression(KQL('strcmp({}, {})'.format(to_kql(expr1), to_kql(expr2))))

    @staticmethod
    def string_size(expr: StringType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/stringsizefunction
        """
        return StringExpression(expr).string_size()

    @staticmethod
    def strlen(expr: StringType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/strlenfunction
        """
        return NumberExpression(KQL('strlen({})'.format(to_kql(expr))))

    @staticmethod
    def strrep(expr: StringType,
               multiplier: NumberType,
               delimiter: StringType = None) -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/strrepfunction
        """
        if delimiter is None:
            res = 'strrep({}, {})'.format(to_kql(expr), to_kql(multiplier))
        else:
            res = 'strrep({}, {}, {})'.format(to_kql(expr), to_kql(multiplier),
                                              to_kql(delimiter))
        return StringExpression(KQL(res))

    @staticmethod
    def substring(expr: StringType, start_index: NumberType, length: NumberType = None) -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/substringfunction
        """
        return StringExpression(KQL(
            ('substring({}, {})' if length is None else 'substring({}, {}, {})').format(
                to_kql(expr), to_kql(start_index), to_kql(length)
            )
        ))

    # def tan(self): return
    #
    #
    # def tdigest_merge(self): return

    @staticmethod
    def to_bool(expr: ExpressionType) -> BooleanExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/toboolfunction
        """
        return BooleanExpression(KQL('tobool({})'.format(to_kql(expr))))

    @staticmethod
    def to_datetime(expr: StringType) -> DatetimeExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/todatetimefunction
        """
        return DatetimeExpression(KQL('todatetime({})'.format(to_kql(expr))))

    @staticmethod
    def to_decimal(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/todecimalfunction
        """
        return NumberExpression(KQL("todecimal({})".format(to_kql(expr))))

    @staticmethod
    def to_double(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/todoublefunction
        """
        return NumberExpression(KQL("todouble({})".format(to_kql(expr))))

    @staticmethod
    def to_dynamic() -> DynamicExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/todynamicfunction
        """
        raise NotImplemented  # pragma: no cover

    @staticmethod
    def to_guid() -> AnyExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/toguidfunction
        """
        raise NotImplemented  # pragma: no cover

    @staticmethod
    def to_hex(expr1: NumberType, expr2: NumberType = None) -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/tohexfunction
        """
        return StringExpression(KQL(('tohex({})' if expr2 is None else 'tohex({}, {})').format(to_kql(expr1), to_kql(expr2))))

    @staticmethod
    def to_int(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/tointfunction
        """
        return NumberExpression(KQL("toint({})".format(to_kql(expr))))

    @staticmethod
    def to_long(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/tolongfunction
        """
        return NumberExpression(KQL("tolong({})".format(to_kql(expr))))

    @staticmethod
    def to_lower(expr: StringType) -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/tolowerfunction
        """
        return expr.lower()

    @staticmethod
    def to_real(expr: NumberType) -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/todoublefunction
        """
        return NumberExpression(KQL("toreal({})".format(to_kql(expr))))

    @staticmethod
    def to_string(expr: ExpressionType):
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/tostringfunction
        """
        return expr.to_string()

    @staticmethod
    def to_timespan() -> TimespanExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/totimespanfunction
        """
        raise NotImplemented  # pragma: no cover

    @staticmethod
    def to_upper(expr: StringType) -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/toupperfunction
        """
        return expr.upper()

    # def to_utf8(self): return
    #
    #
    # def translate(self): return
    #
    #
    # def treepath(self): return

    @staticmethod
    def trim() -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/trimfunction
        """
        raise NotImplemented  # pragma: no cover

    # def trim_end(self): return
    #
    #
    # def trim_start(self): return

    @staticmethod
    def url_decode() -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/urldecodefunction
        """
        raise NotImplemented  # pragma: no cover

    @staticmethod
    def url_encode() -> StringExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/urlencodefunction
        """
        raise NotImplemented  # pragma: no cover

    @staticmethod
    def week_of_year() -> NumberExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/weekofyearfunction
        """
        raise NotImplemented  # pragma: no cover

    # def welch_test(self): return

    @staticmethod
    def zip() -> DynamicExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/zipfunction
        """
        raise NotImplemented  # pragma: no cover

    # ----------------------------------------------------
    # Aggregation functions
    # -----------------------------------------------------

    @staticmethod
    def any(*args: ExpressionType) -> AnyAggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/any-aggfunction
        """
        res = 'any({})'.format(', '.join([arg.kql for arg in args]))
        return AnyAggregationExpression(KQL(res))

    @staticmethod
    def arg_max(*args: ExpressionType) -> AnyAggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/arg-max-aggfunction
        """
        res = 'arg_max({})'.format(', '.join([arg.kql for arg in args]))
        return AnyAggregationExpression(KQL(res))

    @staticmethod
    def arg_min(*args: ExpressionType) -> AnyAggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/arg-min-aggfunction
        """
        res = 'arg_min({})'.format(', '.join([arg.kql for arg in args]))
        return AnyAggregationExpression(KQL(res))

    @staticmethod
    def avg(expr: ExpressionType) -> NumberAggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/avg-aggfunction
        """
        return NumberAggregationExpression(KQL('avg({})'.format(to_kql(expr))))

    @staticmethod
    def avg_if(expr: ExpressionType, predicate: BooleanType) -> NumberAggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/avgif-aggfunction
        """
        return NumberAggregationExpression(KQL('avgif({}, {})'.format(to_kql(expr), to_kql(predicate))))

    # def buildschema(self):
    #     return

    @staticmethod
    def count(col: AnyTypeColumn = None) -> NumberAggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/count-aggfunction
        """
        res = "count()" if col is None else "count({})".format(col.kql)
        return NumberAggregationExpression(KQL(res))

    @staticmethod
    def count_if(predicate: BooleanType) -> NumberAggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/countif-aggfunction
        """
        return NumberAggregationExpression(KQL('countif({})'.format(to_kql(predicate))))

    @staticmethod
    def dcount(expr: ExpressionType, accuracy: NumberType = None) -> NumberAggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/dcount-aggfunction
        """
        return NumberAggregationExpression(KQL(
            ('dcount({})' if accuracy is None else 'dcount({}, {})').format(to_kql(expr), to_kql(accuracy))
        ))

    @staticmethod
    def dcount_if(expr: ExpressionType, predicate: BooleanType, accuracy: NumberType = 0) -> NumberAggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/dcountif-aggfunction
        """
        return NumberAggregationExpression(KQL('dcountif({}, {}, {})'.format(
            to_kql(expr), to_kql(predicate), to_kql(accuracy)
        )))

    # def hll(expr: ExpressionType, accuracy: NumberType = None) -> AggregationExpression:
    #     return AggregationExpression(KQL(
    #         ('hll({})' if accuracy is None else 'hll({}, {})').format(expr, accuracy)
    #     ))

    # def hll_merge(expr: ExpressionType) -> AggregationExpression:
    #     return AggregationExpression(KQL('hll_merge({})'.format(to_kql(expr))))

    @staticmethod
    def make_bag(expr: ExpressionType, max_size: NumberType = None) -> MappingAggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/make-bag-aggfunction
        """
        if max_size:
            return MappingAggregationExpression(KQL('make_bag({}, {})'.format(expr, max_size)))
        return MappingAggregationExpression(KQL('make_bag({})'.format(to_kql(expr))))

    @staticmethod
    def make_list(expr: ExpressionType, max_size: NumberType = None) -> ArrayAggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/makelist-aggfunction
        """
        if max_size:
            return ArrayAggregationExpression(KQL('make_list({}, {})'.format(expr, max_size)))
        return ArrayAggregationExpression(KQL('make_list({})'.format(to_kql(expr))))

    @staticmethod
    def make_set(expr: ExpressionType, max_size: NumberType = None) -> ArrayAggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/makeset-aggfunction
        """
        if max_size:
            return ArrayAggregationExpression(KQL('make_set({}, {})'.format(expr, max_size)))
        return ArrayAggregationExpression(KQL('make_set({})'.format(to_kql(expr))))

    @staticmethod
    def max(expr: ExpressionType) -> AggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/makeset-aggfunction
        """
        return AnyAggregationExpression(KQL('max({})'.format(to_kql(expr))))

    @staticmethod
    def min(expr: ExpressionType) -> AggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/min-aggfunction
        """
        return AnyAggregationExpression(KQL('min({})'.format(to_kql(expr))))

    @staticmethod
    def max_if(expr: ExpressionType, predicate: BooleanType) -> AggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/maxif-aggfunction
        """
        return AnyAggregationExpression(KQL(f'maxif({to_kql(expr)}, {to_kql(predicate)})'))

    @staticmethod
    def min_if(expr: ExpressionType, predicate: BooleanType) -> AggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/minif-aggfunction
        """
        return AnyAggregationExpression(KQL(f'minif({to_kql(expr)}, {to_kql(predicate)})'))

    @staticmethod
    def percentile(expr: ExpressionType, per: NumberType) -> AggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/percentiles-aggfunction
        """
        res = 'percentiles({}, {})'.format(expr, to_kql(per))
        return AnyAggregationExpression(KQL(res))

    @staticmethod
    def percentiles(expr: ExpressionType, *pers: NumberType) -> AggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/percentiles-aggfunction
        """
        res = 'percentiles({}, {})'.format(expr.kql, ', '.join([str(to_kql(per)) for per in pers]))
        return AnyAggregationExpression(KQL(res))

    @staticmethod
    def stdev(expr: ExpressionType) -> AggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/stdev-aggfunction
        """
        return AnyAggregationExpression(KQL('stdev({})'.format(to_kql(expr))))

    @staticmethod
    def stdevif(expr: ExpressionType, predicate: BooleanType) -> AggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/stdevif-aggfunction
        """
        return AnyAggregationExpression(KQL('stdevif({}, {})'.format(to_kql(expr), to_kql(predicate))))

    @staticmethod
    def stdevp(expr: ExpressionType) -> AggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/stdevp-aggfunction
        """
        return AnyAggregationExpression(KQL('stdevp({})'.format(to_kql(expr))))

    @staticmethod
    def sum(expr: ExpressionType) -> AggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/sum-aggfunction
        """
        return AnyAggregationExpression(KQL('sum({})'.format(to_kql(expr))))

    @staticmethod
    def sum_if(expr: ExpressionType, predicate: BooleanType) -> AggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/sumif-aggfunction
        """
        return AnyAggregationExpression(KQL('sumif({}, {})'.format(to_kql(expr), to_kql(predicate))))

    # def tdigest(self):
    #     return
    #
    #
    # def tdigest_merge(self):
    #     return

    @staticmethod
    def variance(expr: ExpressionType) -> AggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/variance-aggfunction
        """
        return AnyAggregationExpression(KQL('variance({})'.format(to_kql(expr))))

    @staticmethod
    def variance_if(expr: ExpressionType, predicate: BooleanType) -> AggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/varianceif-aggfunction
        """
        return AnyAggregationExpression(KQL('varianceif({}, {})'.format(to_kql(expr), to_kql(predicate))))

    @staticmethod
    def variancep(expr: ExpressionType) -> AggregationExpression:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/variancep-aggfunction
        """
        return AnyAggregationExpression(KQL('variancep({})'.format(to_kql(expr))))

    # Used for mv-expand
    @staticmethod
    def to_type(column: BaseColumn, type_name: KustoType) -> ColumnToType:
        """
        https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/mvexpandoperator
        """
        return ColumnToType(column, type_name)
