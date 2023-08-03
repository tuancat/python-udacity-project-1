"""Convert datetimes to and from strings.

NASA's dataset provides timestamps as naive datetimes (corresponding to UTC).

The `cd_to_datetime` function converts a string, formatted as the `cd` field of
NASA's close approach data, into a Python `datetime`

The `datetime_to_str` function converts a Python `datetime` into a string.
Although `datetime`s already have human-readable string representations, those
representations display seconds, but NASA's data (and our datetimes!) don't
provide that level of resolution, so the output format also will not.
"""
import datetime


def cd_to_datetime(calendar_date):
    """_summary_ Convert a NASA-formatted calendar date/time description into a datetime.

    Args:
        calendar_date: A calendar date in YYYY-bb-DD hh:mm format.

    Returns:
        _type_:  A naive `datetime` corresponding to the given calendar date and time.
    """
    return datetime.datetime.strptime(calendar_date, "%Y-%b-%d %H:%M")


def datetime_to_str(dt):
    """_summary_ Convert a naive Python datetime into a human-readable string.

    Args:
        dt: A naive Python datetime.
    Returns:
        _type_: That datetime, as a human-readable string without seconds.
    """
    return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M")
