from typing import Any
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def destination_keyboard(destinations: list[dict[str,Any]]) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру для уточнения направления поиска отелей."""
    keyboard = InlineKeyboardMarkup()

    for destination in destinations:
        btn = InlineKeyboardButton(
            f"📍{destination['label']}",
            callback_data=f"{destination['dest_id']}:{destination['search_type']}"
        )
        keyboard.add(btn)
    return keyboard