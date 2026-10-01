from telebot.types import Message
from loader import bot


@bot.message_handler(func=lambda message: message.text.startswith('/'))
def unknown_command(message: Message) -> None:
    """Выводит сообщение пользователю если была введена неизвестная команда"""
    bot.send_message(
        message.chat.id,
        'Неизвестная команда. ' 
        'Используйте /help для просмотра доступных команд.'
    )