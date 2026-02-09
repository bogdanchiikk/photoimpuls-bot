# Скрипт для подготовки проекта к загрузке на GitHub
# Убирает секретные данные из кода перед коммитом

import re
import shutil
from pathlib import Path

def prepare_bot_py():
    """Убирает токен бота из bot.py для GitHub версии."""
    bot_file = Path("bot.py")
    if not bot_file.exists():
        print("Файл bot.py не найден!")
        return False
    
    with open(bot_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Сохраняем оригинал
    backup_file = Path("bot.py.backup")
    if not backup_file.exists():
        shutil.copy(bot_file, backup_file)
        print("Создан backup: bot.py.backup")
    
    # Убираем токен из кода
    old_line = r'BOT_TOKEN = os\.getenv\("BOT_TOKEN", "[^"]+"\)\.strip\(\)'
    new_line = 'BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()\nif not BOT_TOKEN:\n    raise ValueError("BOT_TOKEN must be set in .env file")'
    
    if re.search(old_line, content):
        content = re.sub(old_line, new_line, content)
        with open(bot_file, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ bot.py подготовлен для GitHub (токен убран)")
        return True
    else:
        print("⚠️ Токен уже убран или формат строки другой")
        return False

def check_secrets():
    """Проверяет, что нет секретов в коде."""
    bot_file = Path("bot.py")
    if not bot_file.exists():
        return
    
    with open(bot_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Проверяем на наличие токенов
    token_patterns = [
        r'\d{10}:[A-Za-z0-9_-]{35}',  # Формат токена Telegram бота
        r'AAEESDjQwRL6BYXMe7TV0nchnJKQ70Wd038',  # Конкретный токен
    ]
    
    found_secrets = []
    for pattern in token_patterns:
        if re.search(pattern, content):
            found_secrets.append(f"Найден токен: {pattern}")
    
    if found_secrets:
        print("⚠️ ВНИМАНИЕ: В коде найдены секреты!")
        for secret in found_secrets:
            print(f"   {secret}")
        print("   Убедитесь, что они не попадут в GitHub!")
    else:
        print("✅ Секреты не найдены в коде")

def restore_backup():
    """Восстанавливает оригинальный bot.py из backup."""
    backup_file = Path("bot.py.backup")
    bot_file = Path("bot.py")
    
    if backup_file.exists():
        shutil.copy(backup_file, bot_file)
        print("✅ bot.py восстановлен из backup")
        return True
    else:
        print("❌ Backup не найден!")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        restore_backup()
    else:
        print("Подготовка проекта для GitHub...")
        print("-" * 50)
        prepare_bot_py()
        check_secrets()
        print("-" * 50)
        print("\n✅ Готово! Теперь можно коммитить и пушить на GitHub.")
        print("\nПосле загрузки на GitHub выполните:")
        print("   python prepare_for_github.py restore")
        print("чтобы восстановить рабочую версию с токеном.")
