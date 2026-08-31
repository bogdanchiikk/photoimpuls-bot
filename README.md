# Photoimpuls Bot

Telegram-бот для конференции: регистрация участников, проверка подписки на канал, выбор специальности и дней, уведомления о готовности фото, запись в Google Sheets, мини-приложение с расписанием.

Автор: **Юлия Богданова** ([@bogdanchiikk](https://github.com/bogdanchiikk))

## Возможности

- проверка подписки на канал
- выбор специальности (сохраняется в SQLite)
- подписка на уведомления по дням конференции
- массовая рассылка ссылок на альбомы
- интеграция с Google Sheets через Apps Script
- веб-расписание на React + TypeScript + Vite

## Стек

Python 3.9+, python-telegram-bot, SQLite, Google Apps Script, React, TypeScript, Vite, Tailwind CSS.

## Структура

```
bot.py                 основной бот
database.py            SQLite
sheets.py              Google Sheets
texts.py               тексты сообщений
google-sheets-script.js
schedule/              React-приложение расписания
images/
scripts/               служебные скрипты деплоя
```

## Запуск

```bash
git clone https://github.com/bogdanchiikk/photoimpuls-bot.git
cd photoimpuls-bot
pip install -r requirements.txt
```

Скопируйте `.env.example` в `.env` и заполните токен бота, id канала и при необходимости URL Google Apps Script.

```bash
python bot.py
```

Расписание:

```bash
cd schedule
npm install
npm run dev
```

Команды организатора: `/notify_day1`, `/notify_day2`, `/notify_day3`, `/notify_ready`.

Секреты только в `.env`, в репозиторий не коммитятся.
