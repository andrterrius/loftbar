import pytz
from datetime import UTC, datetime

msk_tz = pytz.timezone('Europe/Moscow')

def utcnow() -> datetime:
    return datetime.now(UTC)

def format_datetime_msk(dt):
    if not dt: return "-"

    return dt.astimezone(msk_tz).strftime('%d.%m.%Y %H:%M')