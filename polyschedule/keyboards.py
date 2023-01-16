from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback


MAIN = (
    Keyboard(one_time=False, inline=False)
    .add(Text('Сегодня'), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text('Вчера'))
    .add(Text('Неделя'), color=KeyboardButtonColor.POSITIVE)
    .add(Text('Завтра'))
    .row()
    .add(Text('Создать дедлайн'))
).get_json()


WEEK = (
    Keyboard(inline=True)
    .add(Callback('<', {'cmd': 'previous'}))
    .add(Callback('>', {'cmd': 'next'}), color=KeyboardButtonColor.POSITIVE)
).get_json()


DEADLINE = (
    Keyboard(inline=True)
    .add(Callback('<', {'cmd': 'previous'}))
    .add(Callback('>', {'cmd': 'next'}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text('Пн'))
    .add(Text('Вт'))
    .add(Text('Ср'))
    .add(Text('Чт'))
    .row()
    .add(Text('Пт'))
    .add(Text('Сб'))
    .add(Text('Вс'))
).get_json()
