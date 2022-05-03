import datetime


def datetime_wrapper(date):
    if isinstance(date, datetime.date):
        return(datetime.datetime(date.year, date.month, date.day))
    else:
        return(date)

def today_add(day=0) -> datetime:
    today = datetime.date.today()
    today = today + datetime.timedelta(days=day)
    return(datetime_wrapper(today))

def create_date_mapping(day_count=5):
    days = {today_add(-i):{'string':f"{i} days ago", 'day': -i} for i in range(day_count)}
    days[today_add(0)]['string'] = "Today"
    days[today_add(-1)]['string'] = "Yesterday"
    return days
