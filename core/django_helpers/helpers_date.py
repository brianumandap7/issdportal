from datetime import datetime, timedelta

def now():
    return datetime.now()

def today():
    return datetime.today().date()

def format_date(date_obj, fmt="%Y-%m-%d"):
    return date_obj.strftime(fmt) if date_obj else None

def parse_date(date_str, fmt="%Y-%m-%d"):
    try:
        return datetime.strptime(date_str, fmt)
    except (ValueError, TypeError):
        return None

def add_days(date_obj, days):
    return date_obj + timedelta(days=days)

def diff_days(date1, date2):
    return (date2 - date1).days
