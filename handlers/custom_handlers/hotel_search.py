from datetime import datetime, timedelta

from telegram_bot_calendar import DetailedTelegramCalendar
from telebot.types import Message, CallbackQuery

from api.hotels_api import (
    search_destination,
    search_hotels
)
from database.models import Search
from loader import bot
from states.hotels_states import HotelStates
from keyboards.inline import (
    children_keyboard,
    destination_keyboard,
    pagination_keyboard
)
from utils.misc.hotel_sender import send_hotels


def start_hotel_search(user_id: int, chat_id: int, search_mode: str) -> None:
    """Запускает сценарий поиска отелей."""
    bot.set_state(user_id, HotelStates.city, chat_id)
    with bot.retrieve_data(user_id, chat_id) as data:
        data["search_mode"] = search_mode
    bot.send_message(chat_id, 'Введите город')


@bot.callback_query_handler(
        func=lambda callback:
        callback.data in ['lowprice', 'guest_rating','bestdeal']
    )
def hotel_search(callback: CallbackQuery) -> None:
    """Запускает сценарий поиска отелей."""
    start_hotel_search(callback.from_user.id, callback.message.chat.id, callback.data)


@bot.message_handler(commands=["lowprice", "guest_rating", "bestdeal"])
def command_hotel_search(message: Message) -> None:
    """Запускает сценарий поиска отелей."""
    start_hotel_search(message.from_user.id, message.chat.id, message.text.lstrip('/'))


@bot.message_handler(state=HotelStates.city)
def get_city(message: Message) -> None:
    """Получает от пользователя город и уточняет местоположение"""
    result = search_destination(message.text)
    if result:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text    
        keyboard = destination_keyboard(result['data'])
        bot.send_message(message.chat.id, 'Уточните местоположение', reply_markup=keyboard)
    else:
       bot.send_message(message.chat.id, 'Возникла ошибка. Попробуйте позже')


@bot.callback_query_handler(func=lambda callback: ':' in callback.data)
def select_destination(callback: CallbackQuery) -> None:
    """Получает местоположение через инлайн-клавиаутру. Уточняет количество взрослых"""
    dest_id, destination_type = callback.data.split(':')
    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        data['dest_id'] = dest_id
        data['destination_type'] = destination_type
    bot.set_state(callback.from_user.id, HotelStates.adults, callback.message.chat.id)
    bot.send_message(callback.message.chat.id, 'Введите количество взрослых(цифрой)')


@bot.message_handler(state=HotelStates.adults)
def get_adults(message: Message) -> None:
    """Получает количество взрослых. Уточняет есть ли дети среди гостей"""
    if message.text.isdigit() and int(message.text) > 0:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['adults'] = int(message.text)
    else:
       bot.send_message(message.chat.id, 'Введите количество гостей цифрой') 
       return
    
    keyboard = children_keyboard()
    bot.send_message(message.chat.id, 'Есть ли дети?',reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data in ['yes', 'no'])
def has_children(callback: CallbackQuery) -> None:
    """Уточняет возраст детей, если они есть, или переходит к уточнению минимальной цены"""
    bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    
    if callback.data == 'yes':
        bot.set_state(callback.from_user.id, HotelStates.children_age, callback.message.chat.id)
        bot.send_message(callback.message.chat.id, 'Введите возраст детей через запятую')
    else:
        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:    
            data['children_age'] = ''
        bot.set_state(callback.from_user.id, HotelStates.min_price, callback.message.chat.id)
        bot.send_message(callback.message.chat.id, 'Введите минимальную цену проживания')


@bot.message_handler(state=HotelStates.children_age)
def get_age_children(message: Message) -> None:
    """Получает возраст детей. Уточняет минимальную стоимость проживания"""
    ages = message.text.split(',')
    children_ages = []
    for age in ages:
        age = age.strip()
        if not age.isdigit():
            bot.send_message(
                message.chat.id,
                'Введите возраст детей цифрами через запятую. Например: 5, 12'
            )
            return
        age = int(age)
        if age < 0 or age > 17:
            bot.send_message(message.chat.id, 'Возраст ребёнка должен быть от 0 до 17 лет')
            return
        children_ages.append(str(age))
    children_ages = ','.join(children_ages)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['children_age'] = children_ages
    bot.set_state(message.from_user.id, HotelStates.min_price, message.chat.id)
    bot.send_message(message.chat.id, 'Введите минимальную стоимость проживания')


@bot.message_handler(state=HotelStates.min_price)
def get_min_price(message: Message) -> None:
    """Получает минимальную стоимость проживания. Уточняет максимальную стоимость проживания"""
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['min_price'] = int(message.text)
    else:
        bot.send_message(message.chat.id, 'Введите стоимость числом')
        return
    bot.set_state(message.from_user.id, HotelStates.max_price, message.chat.id)
    bot.send_message(message.chat.id, 'Введите максимальную стоимость проживания')


@bot.message_handler(state=HotelStates.max_price)
def get_max_price(message: Message) -> None:
    """Получает максимальную стоимость проживания. Уточняет дату въезда"""
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'Введите стоимость числом')
        return
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        max_price = int(message.text)
        if max_price < data['min_price']:
            bot.send_message(
                message.chat.id,
                'Максимальная стоимость не может быть меньше минимальной'
            )
            return
        data['max_price'] = max_price
    today = datetime.now().date()    
    calendar, step = DetailedTelegramCalendar(calendar_id=1, min_date=today).build()
    bot.send_message(message.chat.id, 'Введите дату въезда',reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def get_date_check_in(callback: CallbackQuery) -> None:
    """Получает дату въезда. Уточняет дату выезда"""
    today = datetime.now().date()
    result, key, step = DetailedTelegramCalendar(
        calendar_id=1,
        min_date=today
    ).process(callback.data)
    if result:
        if result < today:
            bot.send_message(
                callback.message.chat.id,
                'Дата въезда не может быть в прошлом.'
            )
            calendar, step = DetailedTelegramCalendar(
                calendar_id=1,
                min_date=today
            ).build()
            bot.send_message(
                callback.message.chat.id,
                'Выберите другую дату въезда',
                reply_markup=calendar
            )
            return
        bot.edit_message_text(
            f'Дата въезда: {result}',
            callback.message.chat.id,
            callback.message.message_id
        )
        with bot.retrieve_data(
            callback.from_user.id,
            callback.message.chat.id
        ) as data:
            data['check_in'] = result
        min_check_out = result + timedelta(days=1)
        calendar, step = DetailedTelegramCalendar(
            calendar_id=2,
            min_date=min_check_out
        ).build()
        bot.send_message(
            callback.message.chat.id,
            'Введите дату выезда',
            reply_markup=calendar
        )
    else:
        bot.edit_message_text('Введите дату въезда',callback.message.chat.id,
                    callback.message.message_id,reply_markup=key)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def get_date_check_out(callback: CallbackQuery) -> None:
    """Получает дату выезда. Делает запрос отелей и выводит их с пагинацией"""
    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        min_check_out = data['check_in'] + timedelta(days=1)
        result, key, step = DetailedTelegramCalendar(
            calendar_id=2,
            min_date=min_check_out
        ).process(callback.data)
        if result:
            if result <= data['check_in']:
                bot.send_message(
                    callback.message.chat.id,
                    'Дата выезда должна быть позже даты заезда'
                )
                calendar, step = DetailedTelegramCalendar(
                    calendar_id=2,
                    min_date=min_check_out
                ).build()
                bot.send_message(
                    callback.message.chat.id,
                    'Выберите другую дату выезда',
                    reply_markup=calendar
                )
                return
            bot.edit_message_text(
                f'Дата выезда: {result}',
                callback.message.chat.id,
                callback.message.message_id
            )
            data['check_out'] = result
            bot.send_message(callback.message.chat.id, 'Спасибо за информацию. Начинаю поиск.')
            
            search_hotel = search_hotels(
            adults=data['adults'],
            children_age=data['children_age'],
            min_price=data['min_price'],
            max_price=data['max_price'],
            dest_id=data['dest_id'],
            destination_type=data['destination_type'],
            check_in=data['check_in'],
            check_out=data['check_out'],
            search_mode=data['search_mode']
            )
            if search_hotel:
                hotels = search_hotel['data']['hotels']
                if not hotels:
                    bot.send_message(
                        callback.message.chat.id,
                        'По заданным параметрам ничего не найдено'
                    )
                    return

                search = Search.create(
                    user_id = callback.from_user.id,
                    city=data['city'],
                    check_in=data['check_in'],
                    check_out=data['check_out']    
                )
                data['search_id'] = search.id
                data['hotels'] = hotels
                data['page'] = 0

                send_hotels(
                    callback.message.chat.id,
                    hotels[:3],
                    data['check_in'],
                    data['check_out'],
                    data['search_id']
                )

                keyboard = pagination_keyboard(
                    page=data['page'],
                    total_hotels=len(data['hotels'])
                )
                bot.send_message(
                    callback.message.chat.id,
                    f'Страница {data["page"]+1}',
                    reply_markup=keyboard
                )
            else:
                bot.send_message(
                    callback.message.chat.id,
                    'Возникла ошибка. Попробуйте позже.'
                )
        else:
            bot.edit_message_text('Введите дату выезда',callback.message.chat.id,
                        callback.message.message_id,reply_markup=key)


@bot.callback_query_handler(func=lambda callback: callback.data == 'next')
def next(callback: CallbackQuery) -> None:
    """Выводит следующие отели при нажатии кнопки"""
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    bot.answer_callback_query(callback.id)
    with bot.retrieve_data(user_id, chat_id) as data:
        data['page'] += 1

        page = data['page']
        hotels = data['hotels']

        start = page * 3
        end = start + 3
        page_hotels = hotels[start:end]

        send_hotels(
            chat_id,
            page_hotels,
            data['check_in'],
            data['check_out'],
            data['search_id']
        )
        bot.edit_message_reply_markup(chat_id, callback.message.message_id, reply_markup=None)
        keyboard = pagination_keyboard(page, len(hotels))

        bot.send_message(chat_id, f'Страница {page+1}', reply_markup=keyboard)
    