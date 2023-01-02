import asyncio
import rapidjson
from vkbottle import PhotoMessageUploader
import polyschedule.utils.image as image
import polyschedule.utils.keyboards as keyboards
import polyschedule.utils.schedule as schedule
from polyschedule.exceptions import GettingScheduleError
from config import api


async def generate_day_message(day_date, group_id="35390") -> dict:
    try:
        day = await schedule.get_day(group_id, date=day_date)

        if not day:
            return {"message": "На этот день расписания нет"}

        uploader = await PhotoMessageUploader(api).upload(image.generate(day, icon=True))
        payload = rapidjson.dumps({"day_date": day_date})

        return {"attachment": uploader, "keyboard": keyboards.MAIN, "payload": payload}
    except GettingScheduleError:
        return {"message": "Ошибка получения расписания с сервера Политеха"}


async def generate_week_message(day_date, group_id="35390") -> dict:
    try:
        week_info, week_schedule = await schedule.get_week(group_id, date=day_date)

        date_start = week_info["date_start"]
        date_end = week_info["date_end"]
        is_odd = "нечётная" if "is_odd" else "чётная"

        payload = rapidjson.dumps({"day_date": day_date})

        if not week_schedule:
            return {"message": f"На неделю {date_start} - {date_end} ({is_odd}) расписания нет", "keyboard": keyboards.WEEK, "payload": payload}

        async def get_uploader(schedule):
            return await PhotoMessageUploader(api).upload(image.generate(schedule, min_height=700))

        tasks = []
        for day_schedule in week_schedule:
            task = get_uploader(day_schedule)
            tasks.append(task)
        attachments = await asyncio.gather(*tasks)

        return {"message": f"Расписание на неделю\n{date_start} - {date_end} ({is_odd})", "attachment": attachments, "keyboard": keyboards.WEEK, "payload": payload}
    except GettingScheduleError:
        return {"message": "Ошибка получения расписания с сервера Политеха"}
