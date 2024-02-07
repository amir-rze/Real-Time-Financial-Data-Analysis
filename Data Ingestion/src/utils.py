from datetime import datetime,timedelta


def convert_datetime_to_str(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%S')

def convert_utc_to_Tehran(dt):
    return (dt + timedelta(hours=3,minutes=30))
