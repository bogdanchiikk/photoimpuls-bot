# Инструкция: Как выложить проект на GitHub

## Шаг 1: Создать репозиторий на GitHub

1. Зайдите на https://github.com/
2. Войдите в свой аккаунт (или зарегистрируйтесь)
3. Нажмите кнопку **"+"** в правом верхнем углу → **"New repository"**
4. Заполните:
   - **Repository name:** `photoimpuls-bot` (или другое название)
   - **Description:** "Telegram bot for conference management with Google Sheets integration"
   - Выберите **Public** (чтобы было видно в портфолио)
   - **НЕ** ставьте галочки на "Add a README file", "Add .gitignore", "Choose a license" (у нас уже есть)
5. Нажмите **"Create repository"**

## Шаг 2: Инициализировать Git в проекте

Откройте PowerShell или терминал в папке проекта:

```powershell
cd C:\Users\julia\photoimpuls-bot
```

Проверьте, что Git установлен:

```powershell
git --version
```

Если Git не установлен, скачайте с https://git-scm.com/

## Шаг 3: Инициализировать репозиторий

```powershell
git init
```

## Шаг 4: Подготовить версию для GitHub (уберет токен из кода)

```powershell
python prepare_for_github.py
```

Это создаст версию `bot.py` без токена для безопасной публикации.

## Шаг 5: Добавить все файлы

```powershell
git add .
```

## Шаг 6: Сделать первый коммит

```powershell
git commit -m "Initial commit: Telegram bot for conference management"
```

Если Git просит настроить имя и email:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Шаг 7: Подключить удалённый репозиторий

Скопируйте URL вашего репозитория с GitHub (например: `https://github.com/yourusername/photoimpuls-bot.git`)

```powershell
git remote add origin https://github.com/yourusername/photoimpuls-bot.git
```

(Замените `yourusername` на ваш GitHub username)

## Шаг 8: Загрузить код на GitHub

```powershell
git branch -M main
git push -u origin main
```

Вас попросят ввести логин и пароль GitHub. Если включена двухфакторная аутентификация, используйте Personal Access Token вместо пароля.

## Шаг 9: Восстановить рабочую версию (после загрузки)

После успешной загрузки на GitHub верните токен в код для работы бота:

```powershell
python prepare_for_github.py restore
```

Теперь бот снова работает с токеном в коде.

## Шаг 10: Переименовать README (опционально)

Если хотите использовать README_PORTFOLIO.md как основной README:

```powershell
git mv README.md README_OLD.md
git mv README.md README_OLD.md
git mv README_PORTFOLIO.md README.md
git commit -m "Update README for portfolio"
git push
```

## ✅ Готово!

Ваш проект теперь на GitHub! Ссылка будет: `https://github.com/yourusername/photoimpuls-bot`

---

## Дополнительно: Добавить описание и теги

На странице репозитория на GitHub:
1. Нажмите **"⚙️ Settings"** (справа)
2. Прокрутите вниз до **"Topics"**
3. Добавьте теги: `telegram-bot`, `python`, `react`, `conference-management`, `portfolio`

## Что НЕ будет загружено (благодаря .gitignore)

- `.env` файлы с секретами
- `bot.db` (база данных)
- `*.log` (логи)
- `__pycache__/` (кэш Python)
- `venv/` (виртуальное окружение)

Всё это правильно — секретные данные не должны попадать в публичный репозиторий!
