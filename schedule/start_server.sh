#!/bin/bash
# Скрипт для запуска Python HTTP-сервера для сайта расписания

cd /root/photoimpuls-bot/schedule
python3 -m http.server 8080
