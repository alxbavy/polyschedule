import io
from abc import ABC, abstractmethod

from PIL import Image, ImageFont, ImageDraw

import polyschedule.dates as dates


class _FontStyle:
    HEADING = ImageFont.truetype('./fonts/Comfortaa-Regular.ttf', 35)
    LABEL = ImageFont.truetype('./fonts/Comfortaa-Light.ttf', 22)
    NORMAL = ImageFont.truetype('./fonts/Comfortaa-Regular.ttf', 25)
    SMALL = ImageFont.truetype('./fonts/Comfortaa-Regular.ttf', 18)


class _Color:
    BLACK = (0, 0, 0, 255)
    GRAY = (130, 130, 130, 255)
    GREEN = (74, 179, 76, 255)


class _Background:
    EMPTY = './images/empty_pattern.jpg'
    CIRCLE_ICON = './images/pattern.jpg'


def _get_weekday_by_num(weekday_num: int) -> str:
    return _WEEK_DAYS[weekday_num - 1]


_WEEK_DAYS = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')


class IImageGenerateAlgorythm(ABC):
    @abstractmethod
    def generate(self, day_data):
        pass


class CircleIconImageGenerateAlgorythm(IImageGenerateAlgorythm):
    BACKGROUND: str = _Background.CIRCLE_ICON
    START_DRAWING_POINT: float = 155

    def generate(self, day_data):
        drawing_point = self.START_DRAWING_POINT

        with Image.open(self.BACKGROUND) as image:
            width, height = image.size
            
            draw = ImageDraw.Draw(image)

            CENTER_X = width/2.5
            LEFT_SIDE_X = width/14

            draw.text(
                xy=(CENTER_X, 50),
                text=_get_weekday_by_num(int(day_data['weekday'])), 
                font=_FontStyle.HEADING, 
                fill=_Color.GREEN if day_data['date'] == dates.get_today() else _Color.BLACK
            )  # weekday

            draw.text(
                xy=(CENTER_X, 90), 
                text=day_data['date'], 
                font=_FontStyle.LABEL, 
                fill=_Color.GRAY
            )  # date

            MAX_SUBJECT_LENGTH = 26

            for lesson in day_data['lessons']:
                subject = lesson['subject']
                if len(subject) >= MAX_SUBJECT_LENGTH:
                    subject = subject[:MAX_SUBJECT_LENGTH] + '...'

                with Image.open('./images/clock.jpg') as clock_image:
                    image.paste(clock_image, (int(CENTER_X), drawing_point-2))

                draw.text(
                    xy=(LEFT_SIDE_X, drawing_point), 
                    text=lesson['typeObj']['abbr'],
                    font=_FontStyle.SMALL, 
                    fill=_Color.GRAY
                )  # abbr

                draw.text(
                    xy=(CENTER_X*1.2, drawing_point), 
                    text='{} - {}'.format(lesson['time_start'], lesson['time_end']), 
                    font=_FontStyle.SMALL, 
                    fill=_Color.GRAY
                )  # time

                draw.text(
                    xy=(LEFT_SIDE_X, drawing_point+25), 
                    text=subject, 
                    font=_FontStyle.NORMAL, 
                    fill=_Color.BLACK
                )  # subject

                auditory = lesson['auditories'][0]
                draw.text(
                    xy=(LEFT_SIDE_X, drawing_point+25+35), 
                    text='{}, {}'.format(auditory['building']['abbr'], auditory['name']), 
                    font=_FontStyle.SMALL, 
                    fill=_Color.GRAY
                )  # building

                drawing_point += 95

            buf = io.BytesIO()
            image.crop((0, 0, width, drawing_point)).save(buf, format='JPEG')

            return buf.getvalue()


class SimpleImageGenerateAlgorythm(IImageGenerateAlgorythm):
    BACKGROUND: str = _Background.EMPTY
    START_DRAWING_POINT: float = 155
    MIN_LENGTH = 700

    def generate(self, day_data):
        drawing_point = self.START_DRAWING_POINT

        with Image.open(self.BACKGROUND) as image:
            width, height = image.size

            draw = ImageDraw.Draw(image)

            CENTER_X = width/2.5
            LEFT_SIDE_X = width/14

            draw.text(
                xy=(LEFT_SIDE_X, 50),
                text=_get_weekday_by_num(int(day_data['weekday'])), 
                font=_FontStyle.HEADING, 
                fill=_Color.GREEN if day_data['date'] == dates.get_today() else _Color.BLACK
            )  # weekday

            draw.text(
                xy=(LEFT_SIDE_X, 90), 
                text=day_data['date'], 
                font=_FontStyle.LABEL, 
                fill=_Color.GRAY
            )  # date

            MAX_SUBJECT_LENGTH = 26

            for lesson in day_data['lessons']:
                subject = lesson['subject']
                if len(subject) >= MAX_SUBJECT_LENGTH:
                    subject = subject[:MAX_SUBJECT_LENGTH] + '...'

                with Image.open('./images/clock.jpg') as clock_image:
                    image.paste(clock_image, (int(width/2.5), drawing_point-2))

                draw.text(
                    xy=(CENTER_X*1.2, drawing_point), 
                    text='{} - {}'.format(lesson['time_start'], lesson['time_end']), 
                    font=_FontStyle.SMALL, 
                    fill=_Color.GRAY
                )  # time

                draw.text(
                    xy=(LEFT_SIDE_X, drawing_point), 
                    text=lesson['typeObj']['abbr'],
                    font=_FontStyle.SMALL, 
                    fill=_Color.GRAY
                )  # abbr

                draw.text(
                    xy=(LEFT_SIDE_X, drawing_point+25), 
                    text=subject, 
                    font=_FontStyle.NORMAL, 
                    fill=_Color.BLACK
                )  # subject

                auditory = lesson['auditories'][0]
                draw.text(
                    xy=(LEFT_SIDE_X, drawing_point+25+35), 
                    text='{}, {}'.format(auditory['building']['abbr'], auditory['name']), 
                    font=_FontStyle.SMALL, 
                    fill=_Color.GRAY
                )  # building

                drawing_point += 95

            buf = io.BytesIO()
            crop_coordinats = (0, 0, width, (max(self.MIN_LENGTH, drawing_point)))
            image.crop(crop_coordinats).save(buf, format='JPEG')

            return buf.getvalue()
