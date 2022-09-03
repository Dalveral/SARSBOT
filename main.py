import COVID19Py
import telebot
from telebot import types

covid19 = COVID19Py.COVID19()
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
        location = covid19.getLocationByCountryCode('US')
    elif get_message_bot == 'россия':
        location = covid19.getLocationByCountryCode('RU')
    elif get_message_bot == 'украина':
        location = covid19.getLocationByCountryCode('UA')
    else:
        location = covid19.getLatest()
        final_message = f"<u>Данные по всему миру:</u>\nЗаболевные: {location['confirmed']:}"

    if final_message == "":
        date = location[0]['last_updated'].split('T')
        time = date[1].split('.')
        final_message = f"<u>Данные по стране {get_message_bot.title()}</u>\nНаселение: {location[0]['country_population']:}\n" \
                        f"Обновление: {date[0]} {time[0]}\n" \
                        f"Заболевшие: {location[0]['latest']['confirmed']:}\n" \
                        f"Смертей: {location[0]['latest']['deaths']:}"

    bot.send_message(message.chat.id, final_message, parse_mode='html')

bot.polling(none_stop=True)
