import io
from abc import ABC, abstractmethod

from PIL import Image, ImageFont, ImageDraw

import polyschedule.dates as dates
from polyschedule.image_tools.utils import Background, Color, FontStyle, START_PIXEL, get_weekday_by_num


class IImageGenerateAlgorythm(ABC):
    @abstractmethod
    def generate(self, day_data):
        pass


class CircleIconImageGenerateAlgorythm(IImageGenerateAlgorythm):
    background: str = Background.CIRCLE_ICON

    def generate(self, day_data):
        pixel = START_PIXEL

        with Image.open(self.background) as image:
            width, height = image.size
            
            draw = ImageDraw.Draw(image)

            draw.text(
                xy=(width/(2.5), 50),
                text=get_weekday_by_num(int(day_data['weekday'])), 
                font=ImageFont.truetype(FontStyle.REGULAR, 35), 
                fill=Color.GREEN if day_data['date'] == dates.get_today() else Color.BLACK
            )  # weekday

            draw.text(
                xy=(width/(2.5), 90), 
                text=day_data['date'], 
                font=ImageFont.truetype(FontStyle.LIGHT, 22), 
                fill=Color.GRAY
            )  # date

            for lesson in day_data['lessons']:
                subject = lesson['subject']
                if len(subject) >= 26:
                    subject = subject[:26] + '...'

                with Image.open('./images/clock.jpg') as clock_image:
                    image.paste(clock_image, (int(width/2.5), pixel-2))

                draw.text(
                    xy=(width/2.5*1.2, pixel), 
                    text='{} - {}'.format(lesson['time_start'], lesson['time_end']), 
                    font=ImageFont.truetype(FontStyle.REGULAR, 18), 
                    fill=Color.GRAY
                )  # time

                draw.text(
                    xy=(width/14, pixel), 
                    text=lesson['typeObj']['abbr'],
                    font=ImageFont.truetype(FontStyle.REGULAR, 18), 
                    fill=Color.GRAY
                )  # abbr

                draw.text(
                    xy=(width/14, pixel+25), 
                    text=subject, 
                    font=ImageFont.truetype(FontStyle.REGULAR, 25), 
                    fill=Color.BLACK
                )  # subject

                auditory = lesson['auditories'][0]
                draw.text(
                    xy=(width/14, pixel+25+35), 
                    text='{}, {}'.format(auditory['building']['abbr'], auditory['name']), 
                    font=ImageFont.truetype(FontStyle.REGULAR, 18), 
                    fill=Color.GRAY
                )  # building

                pixel += 95

            buf = io.BytesIO()
            image.crop((0, 0, width, pixel)).save(buf, format='JPEG')

            return buf.getvalue()


class SimpleImageGenerateAlgorythm(IImageGenerateAlgorythm):
    background: str = Background.EMPTY

    def generate(self, day_data):
        pixel = START_PIXEL

        with Image.open(self.background) as image:
            width, height = image.size

            draw = ImageDraw.Draw(image)

            draw.text(
                xy=(width/(14), 50),
                text=get_weekday_by_num(int(day_data['weekday'])), 
                font=ImageFont.truetype(FontStyle.REGULAR, 35), 
                fill=Color.GREEN if day_data['date'] == dates.get_today() else Color.BLACK
            )  # weekday

            draw.text(
                xy=(width/(14), 90), 
                text=day_data['date'], 
                font=ImageFont.truetype(FontStyle.LIGHT, 22), 
                fill=Color.GRAY
            )  # date

            for lesson in day_data['lessons']:
                subject = lesson['subject']
                if len(subject) >= 26:
                    subject = subject[:26] + '...'

                with Image.open('./images/clock.jpg') as clock_image:
                    image.paste(clock_image, (int(width/2.5), pixel-2))

                draw.text(
                    xy=(width/2.5*1.2, pixel), 
                    text='{} - {}'.format(lesson['time_start'], lesson['time_end']), 
                    font=ImageFont.truetype(FontStyle.REGULAR, 18), 
                    fill=Color.GRAY
                )  # time

                draw.text(
                    xy=(width/14, pixel), 
                    text=lesson['typeObj']['abbr'],
                    font=ImageFont.truetype(FontStyle.REGULAR, 18), 
                    fill=Color.GRAY
                )  # abbr

                draw.text(
                    xy=(width/14, pixel+25), 
                    text=subject, 
                    font=ImageFont.truetype(FontStyle.REGULAR, 25), 
                    fill=Color.BLACK
                )  # subject

                auditory = lesson['auditories'][0]
                draw.text(
                    xy=(width/14, pixel+25+35), 
                    text='{}, {}'.format(auditory['building']['abbr'], auditory['name']), 
                    font=ImageFont.truetype(FontStyle.REGULAR, 18), 
                    fill=Color.GRAY
                )  # building

                pixel += 95

            buf = io.BytesIO()
            image.crop((0, 0, width, (700 if pixel < 700 else pixel))).save(buf, format='JPEG')

            return buf.getvalue()
