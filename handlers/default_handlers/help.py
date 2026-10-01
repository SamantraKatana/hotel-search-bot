from telebot.types import Message
from loader import bot


@bot.message_handler(commands=["help"])
def send_help(message: Message) -> None:
    """Выводит вспомогательное сообщение с доступными командами."""
    help_text = (
        '/lowprice - самые дешёвые отели\n'
        '/guest_rating — отели с лучшим рейтингом\n'
        '/bestdeal — отели ближе к центру\n'
        '/history — история поиска'
    )

    bot.send_message(message.chat.id, help_text)