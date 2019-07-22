import json
from datetime import datetime, timedelta
from typing import Union, Sequence, Mapping, NewType, Type, Dict, Callable, Any

KustoTypes = Union[str, int, bool, datetime, Mapping, Sequence, float, timedelta]
# TODO: Unhandled date types: guid, decimal

KQL = NewType('KQL', str)


def datetime_to_kql(dt: datetime) -> KQL:
    return KQL(dt.strftime('datetime(%Y-%m-%d %H:%M:%S.%f)'))


def timedelta_to_kql(td: timedelta) -> KQL:
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return KQL('time({days}.{hours}:{minutes}:{seconds}.{microseconds})'.format(
        days=td.days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        microseconds=td.microseconds,
    ))


def dynamic_to_kql(d: Union[Mapping, Sequence]) -> KQL:
    return KQL(json.dumps(d))


def bool_to_kql(b: bool) -> KQL:
    return KQL('true') if b else KQL('false')


KQL_CONVERTER_BY_TYPE: Dict[Type, Callable[[Any], KQL]] = {
    datetime: datetime_to_kql,
    timedelta: timedelta_to_kql,
    Mapping: dynamic_to_kql,
    Sequence: dynamic_to_kql,
    bool: bool_to_kql,
}


def to_kql(obj: KustoTypes) -> KQL:
    for kusto_type, converter in KQL_CONVERTER_BY_TYPE.items():
        if isinstance(obj, kusto_type):
            return converter(obj)