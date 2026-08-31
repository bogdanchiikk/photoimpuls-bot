# Скрипт для добавления футера в App.tsx на сервере
# Загрузите этот файл на сервер в /root/photoimpuls-bot/ и выполните: python3 add_footer.py

path = "/root/photoimpuls-bot/schedule/src/App.tsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

footer = '''
      <footer className="mt-16 py-6 border-t border-gray-200 bg-white text-center text-gray-600 text-sm">
        <p className="mb-2">Создано агентством Кафедра</p>
        <img src="/kafedra-logo.png" alt="Кафедра" className="h-12 mx-auto" />
      </footer>
'''

old = """      </main>
    </div>"""
new = """      </main>
""" + footer + """    </div>"""

if old in content:
    content = content.replace(old, new, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Футер добавлен.")
else:
    print("Не найден блок </main> + </div>. Проверьте файл вручную.")
