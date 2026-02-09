# Развертывание сайта расписания на сервере

## Вариант 1: Сборка на сервере (рекомендуется)

Если сборка не работает локально из-за ошибок прав доступа, можно собрать проект прямо на сервере.

### Шаг 1: Загрузить исходники на сервер

**Вариант A: Загрузить во временную папку (если нет прав на /root/photoimpuls-bot/schedule/)**

Из PowerShell на вашем компьютере:

```powershell
# Создать архив с исходниками (исключая node_modules)
cd "C:\Users\julia\Downloads\doctor_bot\doctor_bot\figma"
Compress-Archive -Path "src", "index.html", "package.json", "package-lock.json", "tsconfig.json", "tsconfig.node.json", "vite.config.ts", "tailwind.config.js", "postcss.config.js" -DestinationPath "schedule-source.zip" -Force

# Загрузить на сервер во временную папку
scp schedule-source.zip root@185.198.152.146:/tmp/
```

Затем на сервере (через SSH) переместите файл:

```bash
ssh root@185.198.152.146
mkdir -p /root/photoimpuls-bot/schedule
mv /tmp/schedule-source.zip /root/photoimpuls-bot/schedule/
```

**Вариант B: Сначала создать папку на сервере**

```bash
ssh root@185.198.152.146
mkdir -p /root/photoimpuls-bot/schedule
```

Затем загрузите файл:

```powershell
scp schedule-source.zip root@185.198.152.146:/root/photoimpuls-bot/schedule/
```

### Шаг 2: На сервере - распаковать и собрать

Подключитесь к серверу:

```bash
ssh root@185.198.152.146
```

Выполните на сервере:

```bash
# Создать папку, если её нет
mkdir -p /root/photoimpuls-bot/schedule

# Если файл был загружен в /tmp, переместить его
# mv /tmp/schedule-source.zip /root/photoimpuls-bot/schedule/

cd /root/photoimpuls-bot/schedule

# Распаковать архив
unzip -o schedule-source.zip

# Установить зависимости (если Node.js еще не установлен, установите его)
# Для Ubuntu/Debian:
# curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
# apt-get install -y nodejs

npm install

# Собрать проект
npm run build

# Проверить, что папка dist создана
ls -la dist/
```

### Шаг 3: Запустить Python HTTP-сервер

```bash
cd /root/photoimpuls-bot/schedule
python3 -m http.server 8080
```

**Для запуска в фоне (чтобы работал постоянно):**

```bash
cd /root/photoimpuls-bot/schedule
nohup python3 -m http.server 8080 > /dev/null 2>&1 &
```

**Проверить, что сервер работает:**

```bash
ps aux | grep "python3 -m http.server"
# или
netstat -tlnp | grep 8080
```

**Остановить сервер:**

```bash
pkill -f "python3 -m http.server 8080"
```

---

## Вариант 2: Сборка локально и загрузка готовых файлов

Если сборка работает локально, но была ошибка `EPERM`, попробуйте:

1. **Закрыть все процессы Node.js** (через Диспетчер задач)
2. **Отключить антивирус временно** или добавить папку проекта в исключения
3. **Запустить PowerShell от имени администратора** и выполнить:

```powershell
cd "C:\Users\julia\Downloads\doctor_bot\doctor_bot\figma"
npm run build
```

После успешной сборки загрузите папку `dist` на сервер:

```powershell
scp -r "C:\Users\julia\Downloads\doctor_bot\doctor_bot\figma\dist\*" root@185.198.152.146:/root/photoimpuls-bot/schedule/
```

---

## Проверка работы сайта

После запуска сервера сайт будет доступен по адресу:

**http://185.198.152.146:8080**

Откройте этот адрес в браузере и проверьте, что расписание отображается корректно.

---

## Обновление сайта (после изменений)

### Если собираете на сервере:

```bash
ssh root@185.198.152.146
cd /root/photoimpuls-bot/schedule
# Загрузите новые файлы или сделайте git pull
npm run build
# Сервер уже работает, просто обновите страницу в браузере
```

### Если собираете локально:

```powershell
# На вашем компьютере
cd "C:\Users\julia\Downloads\doctor_bot\doctor_bot\figma"
npm run build

# Загрузить на сервер
scp -r "dist\*" root@185.198.152.146:/root/photoimpuls-bot/schedule/
```

---

## Troubleshooting

### Сайт не открывается

1. **Проверьте, что сервер запущен:**
   ```bash
   ps aux | grep "python3 -m http.server"
   ```

2. **Проверьте, что порт 8080 открыт:**
   ```bash
   netstat -tlnp | grep 8080
   ```

3. **Проверьте файлы в папке schedule:**
   ```bash
   ls -la /root/photoimpuls-bot/schedule/
   # Должен быть файл index.html
   ```

### Белый экран в браузере

1. Откройте консоль браузера (F12) и проверьте ошибки
2. Убедитесь, что все файлы загружены (проверьте вкладку Network)
3. Проверьте, что файлы в папке `dist` имеют правильные пути

### Ошибка при сборке на сервере

1. **Проверьте версию Node.js:**
   ```bash
   node --version
   # Должна быть версия 16 или выше
   ```

2. **Переустановите зависимости:**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

---

## Готово! 🎉

Сайт расписания должен работать на **http://185.198.152.146:8080**
