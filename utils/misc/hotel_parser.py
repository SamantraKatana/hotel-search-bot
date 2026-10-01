from typing import Any


def get_hotel_info(hotel: dict[str, Any]) -> dict[str, Any]:
    """Возвращает информацию об отеле."""
    property_data = hotel['property']

    hotel_info = {
        'hotel_id': hotel['hotel_id'],
        'name': property_data['name'],
        'rating': property_data['reviewScore'],
        'latitude': property_data['latitude'],
        'longitude': property_data['longitude'],
        'price': property_data['priceBreakdown']['grossPrice']['amountRounded'],
    }
    return hotel_info


def get_description(description_data: dict[str, Any]) -> str | None:
    """Возвращает описание отеля или None, если описание не найдено."""
    for item in description_data['data']:
        if item['descriptiontype_id'] == 6:
            return item['description']


def get_url(details_data: dict[str, Any]) -> str:
    """Достаёт ссылку на отель из словаря."""
    return details_data['data']['url']


def get_photos(details_data: dict[str, Any]) -> list[str]:
    """Достаёт ссылки на фотографии."""
    photos = []
    rooms = details_data['data']['rooms']
    for room in rooms.values():
        for photo in room['photos']:
            photos.append(photo['url_max750'])
    return photos

