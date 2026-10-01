import json
from datetime import datetime

from telebot.types import Message, InputMediaPhoto, CallbackQuery
from telebot.apihelper import ApiTelegramException
from peewee import fn
from telegram_bot_calendar import DetailedTelegramCalendar

from loader import bot
from database.models import Search


def show_history_calendar(chat_id: int) -> None:
    """Выводит календарь для выбора даты показа истории."""
    calendar, step = DetailedTelegramCalendar(calendar_id=3).build()
    bot.send_message(
        chat_id,
        'За какое число вывести историю?',
        reply_markup=calendar
    )


@bot.message_handler(commands=["history"])
def send_history(message: Message) -> None:
    """Выводит календарь для выбора даты показа истории."""
    show_history_calendar(message.chat.id)


@bot.callback_query_handler(func=lambda callback: callback.data == 'history')
def history_callback(callback: CallbackQuery) -> None:
    """Выводит календарь для выбора даты показа истории."""
    show_history_calendar(callback.message.chat.id)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=3))
def get_history(callback: CallbackQuery) -> None:
    """Выводит историю поиска."""
    result, key, step = DetailedTelegramCalendar(
        calendar_id=3
    ).process(callback.data)
    if result:
        bot.edit_message_text(
            f'История за {result}',
            callback.message.chat.id,
            callback.message.message_id
        )
        user_id = callback.from_user.id
        searches = Search.select().where(
            (Search.user_id == user_id)
            & (fn.DATE(Search.search_date) == result)
        )
        if not searches.exists():
            bot.send_message(
                callback.message.chat.id,
                'За эту дату история поиска отсутствует.'
            )
            return
        for search in searches:
            bot.send_message(
                callback.message.chat.id,
                f'Город: {search.city}\n'
                f'Дата поиска: {search.search_date}'
            )
            for hotel in search.hotels:
                bot.send_message(
                    callback.message.chat.id,
                    f'Название отеля: {hotel.name}\n'
                    f'Цена: {hotel.price}\n'
                    f'Координаты: {hotel.latitude},{hotel.longitude}\n'
                    f'{hotel.description}\n'
                    f'Ссылка: {hotel.booking_url}\n'
                )
                media = []
                photos = json.loads(hotel.photos)
                for photo_url in photos[:3]:
                    media.append(InputMediaPhoto(photo_url))
                try:
                    if len(media) >= 2:
                        bot.send_media_group(callback.message.chat.id, media)
                    elif len(media) == 1:
                        bot.send_photo(callback.message.chat.id, photos[0])
                except ApiTelegramException as error:
                    with open('log.txt', 'a', encoding='utf-8') as file:
                        file.write(f'{datetime.now()}: {error}\n')
    else:
        bot.edit_message_text(
            'За какое число вывести историю?',
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=key
        )