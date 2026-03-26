import pytz
from datetime import UTC, datetime, date, time, timedelta

msk_tz = pytz.timezone('Europe/Moscow')

def utcnow() -> datetime:
    return datetime.now(UTC)

def msknow() -> datetime:
    return datetime.now(msk_tz)


def get_current_order_date() -> date:
    now_msk = msknow()

    # Если текущее время меньше 3 часов ночи, считаем что это еще предыдущий день
    if now_msk.time() < time(3, 0):
        # Возвращаем вчерашнюю дату
        return (now_msk - timedelta(days=1)).date()
    else:
        # Возвращаем сегодняшнюю дату
        return now_msk.date()

def format_datetime_msk(dt):
    if not dt: return "-"

    return dt.astimezone(msk_tz).strftime('%d.%m.%Y %H:%M')