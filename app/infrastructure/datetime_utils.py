"""Utilities for handling dates and times with Mexico timezone consistently."""

import pytz
from datetime import date, datetime, time

MEXICO_TIMEZONE = pytz.timezone('America/Mexico_City')


def get_mexico_now() -> datetime:
    """Get current datetime in Mexico City timezone."""
    return datetime.now(MEXICO_TIMEZONE)


def get_mexico_today() -> date:
    """Get today's date in Mexico City timezone."""
    return get_mexico_now().date()


def get_mexico_now_time() -> time:
    """Get current time in Mexico City timezone."""
    return get_mexico_now().time()
