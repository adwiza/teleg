import telepot
import random as r

from settings import BOT_TOKEN, CHAT_ID, MY_CHAT_ID

bot = telepot.Bot(BOT_TOKEN)
# message = bot.sendMessage(chat_id=MY_CHAT_ID, text="/fortune")
# bot.pinChatMessage(CHAT_ID, message['message_id'])
# print(bot.getMe())
last_update = bot.getUpdates()


def generate_prophecies():
    """Функция генерирует предсказание."""
    times = ["утром", "днём", "вечером", "ночью", "после обеда", "перед сном"]
    advices = ["ожидайте", "предостерегайтесь", "будьте открыты для"]
    promises = ["гостей из забытого прошлого", "встреч со старыми знакомыми", "неожиданного праздника",
                "приятных перемен"]
    generated_prophecies = []
    i = 0
    while i < 6:
        j = 0
        forecast = []
        while j < 2:
            random_times = r.choice(times)
            random_advices = r.choice(advices)
            random_promises = r.choice(promises)
            full_sentence = random_times.capitalize() + " " + random_advices + " " + random_promises + "."
            forecast.append(full_sentence)
            j += 1
        generated_prophecies.append(forecast[0] + " " + forecast[1])
        i += 1

    return generated_prophecies


text_horoscope = generate_prophecies()
s = r.randint(0, 5)
horo_text = text_horoscope[s]
for item in last_update:
    if item.get('message'):
        if 'text' in item['message']:
            text = item['message']['text']
            if text.startswith("/horo"):
                message = bot.sendMessage(chat_id=CHAT_ID, text=horo_text)
