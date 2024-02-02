from datetime import datetime,timedelta


def convert_datetime_to_str(dt):
    return (dt+timedelta(hours=3,minutes=30)).strftime('%m/%d/%Y %H:%M:%S')

def convert_utc_to_Tehran(dt):
    return (dt + timedelta(hours=3,minutes=30))