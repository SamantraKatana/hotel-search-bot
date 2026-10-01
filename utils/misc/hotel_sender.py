import json
from datetime import date, datetime
from typing import Any

from telebot.apihelper import ApiTelegramException
from telebot.types import InputMediaPhoto

from api.hotels_api import (
    get_hotel_description,
    get_hotel_details
)
from database.models import SearchHotel
from loader import bot
from utils.misc.hotel_parser import (
    get_hotel_info,
    get_description,
    get_url,
    get_photos
)


def send_hotels(
    chat_id: int,
    hotels: list[dict[str, Any]],
    check_in: date,
    check_out: date,
    search_id: int
) -> None:
    """Отправляет сообщение пользователю с информацией об отелях и фото."""
    for hotel in hotels:
        hotel_info = get_hotel_info(hotel)
        description_data = get_hotel_description(hotel_info['hotel_id'])
        if description_data:
            description = get_description(description_data)
        else:
            description = 'Описание недоступно.'  
        details_data = get_hotel_details(hotel_info['hotel_id'], check_in, check_out)
        url = get_url(details_data)
        photos = get_photos(details_data)
        hotel_message = (
            f"🏨 {hotel_info['name']}\n\n"
            f"⭐ Рейтинг: {hotel_info['rating']}\n"
            f"💰 Цена: {hotel_info['price']}\n"
            f"📅 Даты: {check_in} — {check_out}\n"
            f"📍 Координаты: {hotel_info['latitude']}, {hotel_info['longitude']}\n\n"
            f"📝 {description}\n\n"
            f"🔗 {url}"
        )
        SearchHotel.create(
            search=search_id,
            name=hotel_info['name'],
            booking_url=url,
            description=description,
            price=hotel_info['price'],
            photos=json.dumps(photos),
            latitude=hotel_info['latitude'],
            longitude=hotel_info['longitude']
        )
        bot.send_message(chat_id, hotel_message)
        media = []
        for photo_url in photos[:3]:
            media.append(InputMediaPhoto(photo_url))
        try:
            if len(media) >= 2:
                bot.send_media_group(chat_id, media)
            elif len(media) == 1:
                bot.send_photo(chat_id, photos[0])
        except ApiTelegramException as error:
            with open('log.txt', 'a', encoding='utf-8') as file:
                file.write(f'{datetime.now()}: {error}\n')

        