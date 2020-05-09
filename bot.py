import telebot
import config
import logging
from telebot import apihelper
from telebot import types

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ip = '207.97.174.134'
port = '1080'
apihelper.proxy = {'https': 'socks5://{}:{}'.format(ip, port)}
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    """
    Функция, которая присылает стикер и
    выводит приветственное сообщение.
    """
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    # KEYBOARD
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Карты водителя?')
    item2 = types.KeyboardButton('Тахографы?')

    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name} бот</b>,\
    чем могу помочь?'.format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    """
    Функция, которая отвечает,
    на то, что пишется в телеграме.
    """
    if message.chat.type == 'private':
        if message.text == 'Карты водителя?':
            bot.send_message(message.chat.id, str('ЕСТР или СКЗИ?'))
        elif message.text == 'Тахографы?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Хорошо', callback_data='good')
            item2 = types.InlineKeyboardButton('Не очень', callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Отлично, как сам?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Я не знаю, что ответить 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """
    Эта функция реакции на
    настроение пользователя.
    """
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отлично')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, text='Как дела?', reply_markup=None)
            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
