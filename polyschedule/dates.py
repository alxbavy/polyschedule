from datetime import datetime, timedelta


def get_yesterday() -> str:
    return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')


def get_today() -> str:
    return (datetime.now()).strftime('%Y-%m-%d')


def get_tomorrow() -> str:
    return (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')


def get_next_week_day(date) -> str:
    return (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')


def get_prev_week_day(date) -> str:
    return (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=7)).strftime('%Y-%m-%d')
