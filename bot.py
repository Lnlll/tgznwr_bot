import json
from aiogram import Bot, Dispatcher, types
from aiogram import executor

print("Bot запускается...") 

API_TOKEN = '7739793046:AAEHulbFzSWmmOXCJ7qTE1TMnFMKR7u7jmE'  # Вставь сюда свой токен

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

DATA_FILE = 'scripts.json'

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Используй команды:\n"
                        "/add — добавить скрипт\n"
                        "/edit — изменить скрипт\n"
                        "/delete — удалить\n"
                        "или просто отправь название товара")

@dp.message_handler(commands=['add'])
async def add_prompt(message: types.Message):
    await message.reply("Формат:\nНазвание: Джинсы Гориллос\nТекст: Привет! Цена 3500 руб.\n(Можно много строк)")

@dp.message_handler(commands=['edit'])
async def edit_prompt(message: types.Message):
    await message.reply("Формат:\nНазвание: Джинсы Гориллос\nТекст: Новый текст")

@dp.message_handler(commands=['delete'])
async def delete_prompt(message: types.Message):
    await message.reply("Напиши так:\nУдалить: Джинсы Гориллос")

@dp.message_handler(lambda msg: msg.text.startswith("Название:"))
async def save_script(message: types.Message):
    try:
        lines = message.text.split("\n")
        name = lines[0].replace("Название:", "").strip().lower()
        text = "\n".join(lines[1:]).replace("Текст:", "", 1).strip()

        data = load_data()
        data[name] = text
        save_data(data)
        await message.reply(f"Скрипт для «{name}» сохранён.")
    except Exception as e:
        await message.reply(f"Ошибка: {e}")

@dp.message_handler(lambda msg: msg.text.startswith("Удалить:"))
async def delete_script(message: types.Message):
    name = message.text.replace("Удалить:", "").strip().lower()
    data = load_data()
    if name in data:
        del data[name]
        save_data(data)
        await message.reply(f"Скрипт «{name}» удалён.")
    else:
        await message.reply("Такой скрипт не найден.")

@dp.message_handler()
async def find_script(message: types.Message):
    query = message.text.lower()
    data = load_data()
    for name, text in data.items():
        if query in name:
            await message.reply(text)
            return
    await message.reply("Скрипт не найден.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
