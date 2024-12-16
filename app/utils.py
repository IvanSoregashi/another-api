import datetime


def timestamp():
    return str(datetime.datetime.now(datetime.UTC).isoformat())


def current_year_month():
    return timestamp()[:7]


if __name__ == "__main__":
    print(current_year_month())