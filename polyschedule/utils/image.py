import io
from typing import Optional
from PIL import Image, ImageFont, ImageDraw
import polyschedule.utils.dates as dates


class FontStyle:
    REGULAR = "./fonts/Comfortaa-Regular.ttf"
    LIGHT = "./fonts/Comfortaa-Light.ttf"


class Color:
    BLACK = (0, 0, 0, 255)
    GRAY = (130, 130, 130, 255)
    GREEN = (74, 179, 76, 255)


class Background:
    EMPTY = "./images/empty_pattern.jpg"
    CIRCLE = "./images/pattern.jpg"


WEEK_DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
START_PIXEL = 155


def get_weekday_by_num(weekday_num: int) -> str:
    return WEEK_DAYS[weekday_num - 1]


def generate(day_data, icon=False, min_height=0) -> Optional[bytes]:
    if not day_data:
        return None

    pixel = START_PIXEL

    week_day = get_weekday_by_num(int(day_data['weekday']))
    date = day_data['date']
    lessons = day_data["lessons"]

    background = Background.CIRCLE if icon else Background.EMPTY

    with Image.open(background) as image:
        width, height = image.size

        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(FontStyle.REGULAR, 35)
        font_color = Color.GREEN if date == dates.get_today() else Color.BLACK
        draw.text((width/(2.5 if icon else 14), 50), week_day, font=font, fill=font_color)  # weekday

        font = ImageFont.truetype(FontStyle.LIGHT, 22)
        draw.text((width/(2.5 if icon else 14), 90), date, font=font, fill=Color.GRAY)  # date

        for lesson in lessons:
            auditory = lesson["auditories"][0]
            subject = lesson['subject']
            abbr = lesson['typeObj']['abbr']
            time = f"{lesson['time_start']} - {lesson['time_end']}"
            building = f"{auditory['building']['abbr']}, {auditory['name']}"

            if len(subject) >= 26:
                subject = subject[:26] + "..."

            with Image.open("./images/clock.jpg") as image_two:
                image.paste(image_two, (int(width/2.5), pixel-2))

            font = ImageFont.truetype(FontStyle.REGULAR, 18)
            draw.text((width/2.5*1.2, pixel), time, font=font, fill=Color.GRAY)

            font = ImageFont.truetype(FontStyle.REGULAR, 18)
            draw.text((width/14, pixel), abbr, font=font, fill=Color.GRAY)

            font = ImageFont.truetype(FontStyle.REGULAR, 25)
            draw.text((width/14, pixel+25), subject, font=font, fill=Color.BLACK)

            font = ImageFont.truetype(FontStyle.REGULAR, 18)
            draw.text((width/14, pixel+25+35), building, font=font, fill=Color.GRAY)
            pixel += 95

        buf = io.BytesIO()
        image.crop((0, 0, width, (min_height if pixel < min_height else pixel))).save(buf, format='JPEG')

        return buf.getvalue()
