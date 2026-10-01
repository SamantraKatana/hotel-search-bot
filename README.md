# Hotel Search Bot

Бот для поиска отелей в Telegram.

## Возможности

Бот умеет искать отели по заданным параметрам: по цене, датам въезда и выезда, количеству гостей.
Доступен поиск с сортировкой по цене, рейтингу, удалённости от центра.

## Команды

/start - запускает бота. В прикрелённой клавиатуре доступен выбор способа сортировки (по цене, по рейтингу, по удалённости от центра).
/help - выводит в телеграме все доступные команды.
/history - выводит историю поиска.
/lowprice - поиск дешевых отелей.
/guest_rating - выводит отели с лучшим рейтингом.
/bestdeal - ищет отели ближе к центру

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/SamantraKatana/hotel-search-bot.git
```

2. Перейдите в папку проекта:

```bash
cd SkillboxFirstBt
```

3. Создайте виртуальное окружение:

```bash
python -m venv .venv
```

4. Активируйте виртуальное окружение.

Для Windows:

```bash
.venv\Scripts\activate
```

Для Linux/macOS:

```bash
source .venv/bin/activate
```

5. Установите зависимости:

```bash
pip install -r requirements.txt
```

## Настройка

Какие переменные нужно добавить в .env.:

BOT_TOKEN = "Ваш токен для бота, полученный от @BotFather"
RAPID_API_KEY = "Ваш ключ полученный от API по адресу rapidapi.com/apidojo/api/hotels4/"

## Запуск

После установки зависимостей и настройки переменных окружения запустите бота из корневой папки проекта:

```bash
python main.py
```

## Структура проекта

```text
SkillboxFirstBt/
├── api/
│   └── hotels_api.py
├── config_data/
│   └── config.py
├── database/
│   ├── database.py
│   ├── models.py
│   └── create_tables.py
├── handlers/
│   ├── custom_handlers/
│   │   └── hotel_search.py
│   └── default_handlers/
│       ├── start.py
│       ├── help.py
│       └── history.py
├── keyboards/
│   └── inline/
│       ├── children_keyboard.py
│       ├── destination_keyboard.py
│       ├── pagination_keyboard.py
│       └── search_keyboard.py
├── states/
│   └── hotels_states.py
├── utils/
│   └── misc/
│       ├── hotel_parser.py
│       └── hotel_sender.py
├── .env.template
├── loader.py
├── main.py
└── requirements.txt
```

Основные компоненты проекта:

- `api/` — работа с внешним API поиска отелей.
- `config_data/` — загрузка настроек и переменных окружения.
- `database/` — подключение к SQLite и модели Peewee для хранения истории поиска.
- `handlers/` — обработчики команд, сообщений и callback-запросов Telegram.
- `keyboards/` — inline-клавиатуры Telegram-бота.
- `states/` — состояния пользователя во время пошагового поиска отелей.
- `utils/` — вспомогательные функции для обработки данных об отелях и отправки результатов.
- `loader.py` — создание и настройка экземпляра Telegram-бота.
- `main.py` — точка запуска приложения.
- `requirements.txt` — список зависимостей проекта.
