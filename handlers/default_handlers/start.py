from telebot.types import Message

from loader import bot
from keyboards.inline.search_keyboard import search_keyboard


@bot.message_handler(commands=["start"])
def send_welcome(message: Message) -> None:
    """Выводит приветсвенное сообщение с выбором режима поиска отелей"""
    bot.send_message(
        message.chat.id,
        'Привет! Я бот для поиска отелей.',
        reply_markup=search_keyboard()
    )