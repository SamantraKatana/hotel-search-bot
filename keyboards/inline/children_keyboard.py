from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def children_keyboard() -> InlineKeyboardMarkup:
    """Создаёт клавиатуру для выбора наличия детей."""
    keyboard = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton('Да', callback_data='yes')
    btn2 = InlineKeyboardButton('Нет', callback_data='no')

    keyboard.add(btn1, btn2)
    return keyboard