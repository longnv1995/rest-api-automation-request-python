from datetime import datetime, timezone, timedelta


def _basic_datetime_fmt():
    return '%Y-%m-%dT%H:%M:%S.000Z'

def standard_datetime_fmt():
    return '%y-%m-%d %H-%M-%S'

def _current_dt_in_utc_timezone():
    return datetime.now(timezone.utc)

def report_time():
    current_dt = _current_dt_in_utc_timezone().strftime(standard_datetime_fmt())
    return current_dt

def current_time():
    current_dt = _current_dt_in_utc_timezone().strftime(_basic_datetime_fmt())
    return current_dt

def future_time(days=1, hours=0, minutes=0, seconds=0):
    current_dt = _current_dt_in_utc_timezone()
    timedt = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    future_dt = current_dt + timedt
    future_dt_in_fmt = future_dt.strftime(_basic_datetime_fmt())

    return future_dt_in_fmt
    
def passed_time(last_days=-1, last_hours=0, last_minutes=0, last_seconds=0):
    current_dt = _current_dt_in_utc_timezone()
    timedt = timedelta(days=last_days, hours=last_hours, minutes=last_minutes, seconds=last_seconds)
    passed_dt = current_dt + timedt
    passed_dt_in_fmt = passed_dt.strftime(_basic_datetime_fmt())

    return passed_dt_in_fmt

