from vkbottle.bot import Message, BotLabeler

import polyschedule.utils.dates as dates
from polyschedule.utils.message_generators import generate_week_message, generate_day_message


labeler = BotLabeler()


@labeler.message(regex="[0-9]{4}-[0-9]{2}-[0-9]{2}")  # format 0000-00-00
async def message_handler(message: Message):
    message_data = await generate_day_message(day_date=message.text)
    await message.answer(**message_data)


@labeler.message(text="Сегодня")
async def message_handler(message: Message):
    message_data = await generate_day_message(day_date=dates.get_today())
    await message.answer(**message_data)


@labeler.message(text="Вчера")
async def message_handler(message: Message):
    message_data = await generate_day_message(day_date=dates.get_yesterday())
    await message.answer(**message_data)


@labeler.message(text="Завтра")
async def message_handler(message: Message):
    message_data = await generate_day_message(day_date=dates.get_tomorrow())
    await message.answer(**message_data)


@labeler.message(text="Неделя")
async def message_handler(message: Message):
    message_data = await generate_week_message(day_date=dates.get_today())
    await message.answer(**message_data)
