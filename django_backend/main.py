import os
import telebot
from telebot import types, custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from dotenv import load_dotenv
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "job_schedule.settings")
django.setup()
from admin_interface.serializer import check_telegram_id, check_shift_status, check_break_status, create_new_shift, end_new_shift, create_new_break, end_shift_break, see_weekends


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
token = os.getenv('TELEGRAM_TOKEN')
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(token, state_storage=state_storage)


class MyStates(StatesGroup):
    shift_status = State()


# Обработка команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    if check_telegram_id(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        work_button = types.InlineKeyboardButton(
            'Работа',
            callback_data='work_time'
        )
        weekend_button = types.InlineKeyboardButton(
            'Выходные',
            callback_data='see_weekends'
        )
        tickets_button = types.InlineKeyboardButton(
            'Штрафы',
            callback_data='see_tickets'
        )
        markup.add(work_button, weekend_button, tickets_button)
        bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
    else:
         bot.send_message(message.chat.id, 'Вы тут не работаете')


# Формирование меню для работы
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
    end_break_button = types.InlineKeyboardButton(
        'Закончить перерыв',
        callback_data='end_break'
    )
    if check_shift_status(message.chat.id):
        if check_break_status(message.chat.id):
            markup.add(end_break_button)
            text_message = 'Вы на перерыве'
        else:
            markup.add(start_break_button, end_shift_button)
            text_message = 'Ваша смена идёт'
    else:
        markup.add(start_shift_button)
        text_message = 'Ваша смена не идёт'
    bot.send_message(message.chat.id, text_message, reply_markup=markup)


# Начало смены: установка состояния и запрос фотографии
def start_shift(message):
    bot.set_state(message.chat.id, MyStates.shift_status, message.chat.id)
    bot.send_message(message.chat.id, 'Пришлите фотографию рабочего места')


# Обработка фотографии и начало смены
@bot.message_handler(
                    content_types=['photo'], 
                    state=MyStates.shift_status
                    )
def photo_serializer(message):
    file_id = message.photo[-1].file_id
    file_url = bot.get_file_url(file_id=file_id)
    create_new_shift(message.chat.id, file_url)
    bot.send_message(message.chat.id, 'Смена была успешно начата')
    work_menu(message)
    bot.delete_state(message.from_user.id, message.chat.id)


# Завершение смены
def end_shift(message):
    end_new_shift(message.chat.id)
    bot.send_message(message.chat.id, 'Смена была закончена')
    work_menu(message)


# Начало перерыва
def start_break(message):
    create_new_break(message.chat.id)
    bot.send_message(message.chat.id, 'Перерыв был успешно создан')
    work_menu(message)


# Завершение перерыва
def end_break(message):
    end_shift_break(message.chat.id)
    bot.send_message(message.chat.id, 'Перерыв был успешно закончен')
    work_menu(message)


# Просмотр выходных
def weekends_menu(message):
    weekends = see_weekends(message.chat.id)
    bot.send_message(message.chat.id, str(weekends))


# Создание выходного (не реализовано полностью)
def create_weekend(message):
    bot.send_message(message.chat.id, 'Пришлите дату на которую вы хотите поставить выходной в формате: DD/MM/YYYY')


# Обработка inline-кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'work_time':
        work_menu(call.message)
    if call.data == 'start_shift':
        start_shift(call.message)
    if call.data == 'end_shift':
        end_shift(call.message)
    if call.data == 'start_break':
        start_break(call.message)
    if call.data == 'end_break':
        end_break(call.message)
    if call.data == 'see_weekends':
        weekends_menu(call.message)


# Добавление пользовательского фильтра состояний
bot.add_custom_filter(custom_filters.StateFilter(bot))

# Запуск бота в режиме бесконечного опроса
bot.infinity_polling()