import datetime


def datetime_wrapper(date):
    if isinstance(date, datetime.date):
        return(datetime.datetime(date.year, date.month, date.day))
    else:
        return(date)

def today_add(day=0) -> datetime:
    today = datetime.date.today()
    today = today.replace(day=today.day+day)
    return(datetime_wrapper(today))