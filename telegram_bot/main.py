import os
import telebot
from telebot import types
from dotenv import load_dotenv

# from .serializer import check_telegram_id

_SHIFT_STATUS = False
_BREAK_STATUS = False




dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
token = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    # if check_telegram_id(message.from_user.id):
    markup = types.InlineKeyboardMarkup()
    work_button = types.InlineKeyboardButton(
        'Работа',
        callback_data='work_time'
    )
    weekend_button = types.InlineKeyboardButton(
        'Выходные',
        callback_data='put_weekend'
    )
    tickets_button = types.InlineKeyboardButton(
        'Штрафы',
        callback_data='see_tickets'
    )
    markup.add(work_button, weekend_button, tickets_button)
    bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
    # else:
    #     bot.send_message(message.chat.id, 'Вы тут не работаете')


def work_menu(message):
    markup = types.InlineKeyboardMarkup()
    start_shift_button = types.InlineKeyboardButton(
        'Начать смену',
        callback_data='start_shift'
    )
    start_break_button = types.InlineKeyboardButton(
        'Начать перерыв',
        callback_data='start_break'
    )
    end_shift_button = types.InlineKeyboardButton(
        'Закончить смену',
        callback_data='end_shift'
    )
    if not _SHIFT_STATUS:
        markup.add(start_shift_button)
    if not _BREAK_STATUS:
        markup.add(start_break_button)
    markup.add(end_shift_button)
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'work_time':
        work_menu(call.message)

bot.infinity_polling()