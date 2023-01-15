class FontStyle:
    REGULAR = './fonts/Comfortaa-Regular.ttf'
    LIGHT = './fonts/Comfortaa-Light.ttf'


class Color:
    BLACK = (0, 0, 0, 255)
    GRAY = (130, 130, 130, 255)
    GREEN = (74, 179, 76, 255)


class Background:
    EMPTY = './images/empty_pattern.jpg'
    CIRCLE_ICON = './images/pattern.jpg'


def get_weekday_by_num(weekday_num: int) -> str:
    return WEEK_DAYS[weekday_num - 1]


WEEK_DAYS = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')
START_PIXEL = 155
