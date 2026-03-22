import pytz
from datetime import UTC, datetime

msk_tz = pytz.timezone('Europe/Moscow')

def utcnow() -> datetime:
    return datetime.now(UTC)

def format_datetime_msk(dt):
    if not dt: return "-"

    if dt.tzinfo is None:
        dt = msk_tz.localize(dt)
    else:
        dt = dt.astimezone(msk_tz)

    return dt.strftime('%d.%m.%Y %H:%M')