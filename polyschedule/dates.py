from datetime import datetime, timedelta


def get_yesterday():
    return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')


def get_today():
    return (datetime.now()).strftime('%Y-%m-%d')


def get_tomorrow():
    return (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')


def get_next_week_day(date):
    return (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')


def get_prev_week_day(date):
    return (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=7)).strftime('%Y-%m-%d')
