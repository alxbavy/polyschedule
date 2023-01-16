from vkbottle.bot import MessageEvent, BotLabeler
from vkbottle import GroupEventType
import orjson

import polyschedule.dates as dates
from polyschedule.message_generators import generate_week_message
from config import api


labeler = BotLabeler()


CMD_ANNOTATIONS = {
    'previous': dates.get_prev_week_day,
    'next': dates.get_next_week_day
}


@labeler.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=MessageEvent)
async def message_event_handler(event: MessageEvent):
    message = await api.messages.get_by_conversation_message_id(conversation_message_ids=event.conversation_message_id, peer_id=event.peer_id)
    payload = orjson.loads(message.items[0].payload)

    getter_func = CMD_ANNOTATIONS[event.payload['cmd']]
    message_data = await generate_week_message(day_date=getter_func(payload['day_date']))

    await event.edit_message(**message_data)
