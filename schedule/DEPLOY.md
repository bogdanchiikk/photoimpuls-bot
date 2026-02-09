# Развертывание сайта расписания через Python HTTP-сервер

## Шаг 1: Собрать сайт локально

На вашем компьютере (Windows):

```powershell
cd C:\Users\julia\Downloads\doctor_bot\doctor_bot\figma
npm install
npm run build
```

После этого в папке `figma/dist/` будут готовые файлы сайта.

---

## Шаг 2: Загрузить файлы на сервер

Из PowerShell на вашем компьютере:

```powershell
scp -r "C:\Users\julia\Downloads\doctor_bot\doctor_bot\figma\dist\*" root@185.198.152.146:/root/photoimpuls-bot/schedule/
```

---

## Шаг 3: Запустить Python HTTP-сервер на сервере

Подключитесь к серверу:

```bash
ssh root@185.198.152.146
```

Перейдите в папку с сайтом и запустите сервер:

```bash
cd /root/photoimpuls-bot/schedule
python3 -m http.server 8080
```

**Сервер запустится и будет работать в фоне.** Сайт будет доступен по адресу:

**http://185.198.152.146:8080**

---

## Шаг 4: Запустить сервер в фоне (чтобы не держать терминал открытым)

Если хотите, чтобы сервер работал постоянно, даже после закрытия SSH:

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

## Готово! 🎉

Сайт расписания доступен по адресу: **http://185.198.152.146:8080**

**Примечание:** Это простой способ для теста. Если нужен более надёжный вариант с доменом и HTTPS — можно позже настроить Nginx, но для начала этого достаточно.
