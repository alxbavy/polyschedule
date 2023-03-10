import asyncio
from typing import Optional

import rapidjson
from vkbottle import PhotoMessageUploader

import polyschedule.image_tools.image as image
import polyschedule.keyboards as keyboards
import polyschedule.schedule_api as schedule_api
from polyschedule.image_tools.generate_algorythms import SimpleImageGenerateAlgorythm, CircleIconImageGenerateAlgorythm
from polyschedule.exceptions import GettingScheduleError
from config import api


async def generate_day_message(day_date, group_id='35390') -> dict:
    try:
        day_schedule = await schedule_api.get_day(group_id, date=day_date)

        if not day_schedule:
            return {'message': 'На этот день расписания нет'}

        uploader = await PhotoMessageUploader(api).upload(image.generate(day_schedule, CircleIconImageGenerateAlgorythm()))
        payload = rapidjson.dumps({'day_date': day_date})

        return {
            'attachment': uploader, 
            'keyboard': keyboards.MAIN, 
            'payload': payload
        }
    except GettingScheduleError:
        return {'message': 'Ошибка получения расписания с сервера Политеха'}


async def generate_week_message(day_date, group_id='35390') -> dict:
    try:
        week_info, week_schedule = await schedule_api.get_week(group_id, date=day_date)

        date_start = week_info['date_start']
        date_end = week_info['date_end']
        is_odd = 'нечётная' if 'is_odd' else 'чётная'

        payload = rapidjson.dumps({'day_date': day_date})

        if not week_schedule:
            return {
                'message': f'На неделю {date_start} - {date_end} ({is_odd}) расписания нет', 
                'keyboard': keyboards.WEEK, 
                'payload': payload
            }

        async def get_uploader(schedule):
            return await PhotoMessageUploader(api).upload(image.generate(schedule, SimpleImageGenerateAlgorythm()))

        tasks = []
        for day_schedule in week_schedule:
            task = get_uploader(day_schedule)
            tasks.append(task)
        attachments = await asyncio.gather(*tasks)

        return {
            'message': f'Расписание на неделю\n{date_start} - {date_end} ({is_odd})', 
            'attachment': attachments, 
            'keyboard': keyboards.WEEK, 
            'payload': payload
        }
    except GettingScheduleError:
        return {'message': 'Ошибка получения расписания с сервера Политеха'}
