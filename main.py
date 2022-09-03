import COVID19Py
import telebot
from telebot import types

covid19 = COVID19Py.COVID19()
# Your telegram bot token
bot = telebot.TeleBot('')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Во всем мире')
    btn2 = types.KeyboardButton('Россия')
    btn3 = types.KeyboardButton('Украина')
    btn4 = types.KeyboardButton('США')
    markup.add(btn1, btn2, btn3, btn4)
    send_mess = f'Привет, {message.from_user.first_name}!\nВыберите страну из списка.'
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def mess(message):
    final_message = ""
    get_message_bot = message.text.strip().lower()
    if get_message_bot == 'сша':
        location = covid19.getLocationByCountryCode('US', timelines=True)
    elif get_message_bot == 'россия':
        location = covid19.getLocationByCountryCode('RU', timelines=True)
    elif get_message_bot == 'украина':
        location = covid19.getLocationByCountryCode('UA', timelines=True)
    else:
        location = covid19.getLatest()
        final_message = f"<u>Данные по всему миру:</u>\nЗаболевные: {location['confirmed']:}"

    if final_message == "":
        date = location[0]['last_updated'].split('T')
        time = date[1].split('.')
        location_timesline = location[0]['timelines']['confirmed']['timeline']
        location_sorted = sorted(location_timesline.values())[-2]
        full_day = location[0]['latest']['confirmed'] - location_sorted

        final_message = f"<u>Данные по стране {get_message_bot.title()}</u>\nНаселение: {location[0]['country_population']:}\n" \
                        f"<b>Заболевшие</b>\n    Всего: {location[0]['latest']['confirmed']:}\n    За день: {full_day} \n" \
                        f"Смертей: {location[0]['latest']['deaths']:}" \

    bot.send_message(message.chat.id, final_message, parse_mode='html')

bot.polling(none_stop=True)
