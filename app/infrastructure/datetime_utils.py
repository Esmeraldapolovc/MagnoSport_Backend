
import pytz
from datetime import date, datetime, time

MEXICO_TIMEZONE = pytz.timezone('America/Mexico_City')


def get_mexico_now() -> datetime:
    return datetime.now(MEXICO_TIMEZONE)


def get_mexico_today() -> date:
    return get_mexico_now().date()


def get_mexico_now_time() -> time:
    return get_mexico_now().time()
