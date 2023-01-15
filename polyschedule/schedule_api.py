from typing import Tuple, Optional

import aiohttp
import orjson

from polyschedule.exceptions import GettingScheduleError


async def _request_json(group_id, date) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://ruz.spbstu.ru/api/v1/ruz/scheduler/{group_id}?date={date}') as response:
            return orjson.loads(await response.text())


async def get_week(group_id, date) -> Tuple[dict, Optional[list]]:
    week_json = await _request_json(group_id, date)

    if week_json.get('error'):
        raise GettingScheduleError(week_json["text"])

    week_info = week_json['week']
    week_schedule = week_json['days']

    return week_info, week_schedule or None


async def get_day(group_id, date) -> Optional[Tuple[list]]:
    _, week_schedule = await get_week(group_id, date)

    if not week_schedule:
        return None

    matched_day = [i for i in week_schedule if i['date'] == date]

    return matched_day[0] if matched_day else None
