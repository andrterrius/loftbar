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


def its_evening_now() -> bool:
    now_msk = msknow()
    current_time = now_msk.time()

    # Вечер: с 17:00 до 23:59:59
    if current_time >= time(17, 0):
        return True

    # И с 00:00 до 12:00 следующего дня
    if current_time <= time(12, 0):
        return True

    return False

def format_datetime_msk(dt):
    if not dt: return "-"

    return dt.astimezone(msk_tz).strftime('%d.%m.%Y %H:%M')