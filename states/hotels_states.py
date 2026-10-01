from telebot.handler_backends import State, StatesGroup


class HotelStates(StatesGroup):
    """Хранит состояния пользователя во время поиска отелей."""

    city = State()
    adults = State()
    children_age = State()
    min_price = State()
    max_price = State()
