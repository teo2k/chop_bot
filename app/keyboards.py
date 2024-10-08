from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

confirm_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтверждаю, начать опрос',callback_data='confirm')]
])


q_check = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='1. Имя'), KeyboardButton(text='2. Фамилия')],
    [KeyboardButton(text='3. Город'), KeyboardButton(text='4. Возраст')],
    [KeyboardButton(text='5. Номер'), KeyboardButton(text='6. Завершить анкету')]
],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберите соответствующий пункт.')


confirm_ans = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Подтверждаю данные')],
    [KeyboardButton(text='Изменить данные')],
],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберите соответствующий пункт.')

