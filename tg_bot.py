import requests
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold


TG_TOKEN = ''  # BOT TOKEN
OW_TOKEN = ''  # Open Weather (https://openweathermap.org) TOKEN


bot = Bot(token=TG_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
	await message.reply('Отправь мне название города и получишь прогноз погоды!')


@dp.message_handler()
async def get_weather(message: types.Message):
	weather_icon = {
		'Clear': 'Ясно \U00002600',
		'Clouds': 'Облачно \U00002601',
		'Rain': 'Дождь \U00002614',
		'Drizzle': 'Мелкий дождь \U00002614',
		'Thunderstorm': 'Гроза \U000026A1',
		'Snow': 'Снег \U00001F328',
		'Mist': 'Туман \U00001F32B'
	}
	try:
		response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={OW_TOKEN}&units=metric')
		if response.ok:
			data = response.json()
			city = data['name']
			temperature = round(data['main']['temp'], 1)
			weather_descr = data['weather'][0]['main']
			if weather_descr in weather_icon:
				wd = weather_icon[weather_descr]
			else:
				wd = 'Посмотри в окно'
			humidity = data['main']['humidity']
			pressure = data['main']['pressure']
			wind = data['wind']['speed']
			sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
			sunset = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')

			await message.answer(
				# f'<b>{city}</b>\n'
				f'{hbold(city)}\n'
				f'Температура: {temperature} C, {wd}\n'
				f'Влажность: {humidity}%\n'
				f'Давление: {pressure} мм.рт.ст.\n'
				f'Ветер: {wind} м/с\n'
				f'Восход: {sunrise}\n'
				f'Закат: {sunset}\n'
			)
	except Exception as ex:
		await message.answer(ex)


if __name__ == '__main__':
	executor.start_polling(dp)
