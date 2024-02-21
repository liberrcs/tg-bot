import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, Dispatcher, executor, types
open_weather_token = 'f405e3c0be733447126fa2ff789d01f1'
tg_bot_token = "6342248700:AAGyPI2NwBZCjgtjZzaeAs3YpcZcaY5JLxw"

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришли погоду в этом городе!")

@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric")
        data = r.json()


        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lengh_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C°\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.с\nВетер: {wind} м/c\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {lengh_of_the_day}\n"
              f"Хорошего дня!")


    except:
        await message.reply("Проверьте название города ")

if __name__ == '__main__':
    executor.start_polling(dp)