# BiaminoDesk Telegram Bot

Телеграм бот для сбора информации о пользователях с сохранением в Convex базу данных.

## Требования

- Python 3.8+
- Node.js 14+
- npm или yarn

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/AmanBoronbaev8/BiaminoDesk.git
cd BiaminoDesk
```

2. Установите Python зависимости:
```bash
pip install python-telegram-bot convex
```

3. Установите Node.js зависимости:
```bash
npm install
```

## Настройка

1. Создайте проект в [Convex Dashboard](https://dashboard.convex.dev)
2. Скопируйте URL вашего проекта (выглядит как `https://xxx-xxx-xxx.convex.cloud`)
3. Вставьте URL в файл `1BD.py` в переменную `CONVEX_URL`

## Запуск

1. Запустите Convex сервер разработки:
```bash
npx convex dev
```

2. В другом терминале запустите бота:
```bash
python 1BD.py
```

## Структура проекта

- `1BD.py` - основной файл бота
- `convex/` - директория с Convex конфигурацией
  - `schema.js` - схема базы данных
  - `messages.js` - функции для работы с данными
- `package.json` - конфигурация Node.js проекта
- `convex.json` - конфигурация Convex

## Как это работает

1. Бот запрашивает у пользователя:
   - Номер телефона (через специальную кнопку)
   - Текстовое сообщение
2. Данные сохраняются в Convex базу данных
3. Доступ к данным через Convex Dashboard

## Переменные окружения

- `CONVEX_URL` - URL вашего Convex проекта (в файле `1BD.py`)
- `BOT_TOKEN` - токен вашего Telegram бота (в файле `1BD.py`)

## Примечания

- Все поля в базе данных опциональные
- Если какое-то поле не заполнено, используются значения по умолчанию
- Доступ к данным через Convex Dashboard
