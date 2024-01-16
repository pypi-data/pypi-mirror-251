import datetime


def get_isoformat():
    return datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")


def split_list(lst: list, batch_size=100):
    return [lst[i : i + batch_size] for i in range(0, len(lst), batch_size)]
