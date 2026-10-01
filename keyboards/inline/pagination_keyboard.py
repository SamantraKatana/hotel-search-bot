from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def pagination_keyboard(page: int, total_hotels: int) -> InlineKeyboardMarkup:
    """Создаёт клавиатуру для переключения на следующие варианты отелей (для пагинации)."""
    keyboard = InlineKeyboardMarkup()

    if (page + 1) * 3 < total_hotels:
        btn_next = InlineKeyboardButton('Показать ещё →', callback_data='next')
        keyboard.add(btn_next)
    return keyboard