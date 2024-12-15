import datetime


def timestamp():
    return str(datetime.datetime.now(datetime.UTC).isoformat())
