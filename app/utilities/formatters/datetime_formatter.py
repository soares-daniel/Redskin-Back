from datetime import datetime
from pytz import timezone


def format_datetime_into_isoformat(date_time: datetime) -> str:
    return date_time.replace(tzinfo=timezone("Europe/Paris")).isoformat().replace("+00:00", "Z")
