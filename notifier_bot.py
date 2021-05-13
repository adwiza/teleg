import configparser

import config
import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter
from stopgame import StopGame

logging.basicConfig(level=logging.INFO)

# # Считываем учетные данные
# config = configparser.ConfigParser()
# config.read("config.ini")
#
# # Присваиваем значения внутренним переменным
# api_id = config['Telegram']['api_id']
# api_hash = config['Telegram']['api_hash']
# username = config['Telegram']['username']

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# Инициализируем соединение с БД
db = SQLighter('subscriptions.db')

# инициализируем парсер
sg = StopGame('lastkey.txt')

# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def echo(message: types.Message):
    if not db.subscribers_exists(message.from_user.id):
        # если юзера нет в базе - добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer('Вы успешно подписаны на рассылку!\nЖдите, скоро выйдут новые обзоры.')


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscribers_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его с неактивной подпиской
        db.add_subscriber(message.from_user.id, False)
        await message.answer('Вы итак не полпсианы')
    else:
        # если уон уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer('Вы успешно отписаны от рассылки')


async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        # проверяем наличие новых игр
        new_games = sg.new_games()

        if (new_games):
            # если игры есть, переворачиваем список и итерируем
            new_games.reverse()
            for ng in new_games:
                # парсим инфу о новой игре
                nfo = sg.game_info(ng)

                # получаем список подписчиков бота
                subscriptions = db.get_subscriptions()

                # отправляем всем новость
                with open(sg.download_image(nfo['image']), 'rb') as photo:
                    for s in subscriptions:
                        await bot.send_photo(
                            s[1],
                            photo,
                            caption=nfo['title'] + "\n" + "Оценка: " + nfo['score'] + "\n" + nfo['excerpt'] + "\n\n" +
                                    nfo['link'],
                            disable_notification=True
                        )

                # обновляем ключ
                sg.update_lastkey(nfo['id'])

if __name__ == '__main__':
    dp.loop.create_task(scheduled(10))
    executor.start_polling(dp, skip_updates=True)
