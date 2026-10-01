from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def search_keyboard() -> InlineKeyboardMarkup:
    """Создаёт клавиатуру для начала поиска отелей."""
    keyboard = InlineKeyboardMarkup()

    lowprice_button = InlineKeyboardButton(
        '💰Дешёвые отели',
        callback_data='lowprice'
    )
    guest_rating_button = InlineKeyboardButton(
        '🥇Лучший рейтинг',
        callback_data='guest_rating'
    )
    bestdeal_button = InlineKeyboardButton(
        '📍Ближе к центру',
        callback_data='bestdeal'
    )
    history_button = InlineKeyboardButton(
        '📜История запросов',
        callback_data='history'
    )

    keyboard.add(lowprice_button)
    keyboard.add(guest_rating_button)
    keyboard.add(bestdeal_button)
    keyboard.add(history_button)
    return keyboard