import datetime

import telebot
from telebot import apihelper, TeleBot, types

import func
import client as c
import inline
import markups as m
from markups import back
from APIconst import *
from dbhelper import DBHelper

"""--------------------------------------------------------------------------------------------"""
bot: TeleBot = telebot.TeleBot(API_TOKEN)  # передача токена
apihelper.proxy = {'https': proxy1}
now = datetime.datetime.now()
print(bot.get_me())
db = DBHelper()
"""--------------------------------------------------------------------------------------------"""


@bot.message_handler(commands=['start'])  # приветственное сообщение
def send_welcome(message):
    func.log(message, "START")

    user = db.get_userinfo(0, message.chat.id)
    rank = 'R'

    if user is not None:
        db.setUsername(message.chat.username, message.chat.id)
        bot.send_message(message.chat.id, "Привет, тут ты можешь записаться на сеанс татуировки к @bobatattoo",
                         reply_markup=m.make_markup_menu(user.Rank))
    else:
        db.new_user(str(message.from_user.id), message.chat.username,
                    message.from_user.first_name, message.from_user.last_name, rank)
        Mmenu = m.make_markup_menu('R')
        bot.send_message(message.chat.id, "Привет, тут ты можешь записаться на сеанс татуировки к @bobatattoo",
                         reply_markup=Mmenu)


@bot.message_handler(commands=['admin'])
def check_admin(message):
    if message.chat.id == 310756347:
        panel = m.admin_panel()
        bot.send_message(310756347, "Чего желаете мой господин?", reply_markup=panel)


@bot.message_handler(commands=['key'])
def key(message):
    user = db.get_userinfo(0, message.chat.id)
    kkey = m.make_markup_menu(user.Rank)
    bot.send_message(user.user_id, "Панель для ранга - {}".format(user.Rank), reply_markup=kkey)


@bot.message_handler(regexp="📆Запись")  # действия по нажатии кнопки "Запись"
def handle_message1(message):
    answer = "Запись"
    func.log(message, answer)
    m.main_note_menu(message)


@bot.message_handler(regexp="💎Работы мастера")
def handle_message2(message):
    answer = "Отзывы"
    func.log(message, answer)
    bot.send_message(message.chat.id, "https://www.instagram.com/bobatattoo/")


@bot.message_handler(regexp="⚙Настройки")
def handle_message3(message):
    answer = "Настройки"

    func.log(message, answer)

    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=m.make_settings_keyboard())


@bot.message_handler(regexp="✉Написать мастеру")
def write_master(message):
    answer = "Написать лично"
    func.log(message, answer)
    bot.send_message(message.chat.id, "Напиши мастеру напрямую: @bobatattoo")


@bot.message_handler(content_types=['contact'])
def contact(message):
    phone = c.PhoneRefactor(str(message.contact.phone_number))
    db.set_phone(phone, message.chat.id)
    bot.send_message(message.chat.id, "Введите ваше имя:")
    bot.register_next_step_handler(message, InputName)


@bot.message_handler(regexp="👬Клиенты")
def clientele(message):
    answer = "Клиенты"
    func.log(message, answer)
    c.create_client_menu(message)


"_INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE_"
"_INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE_"


@bot.callback_query_handler(func=lambda call: True)
def inline_main(call):
    answer = "Inline"
    func.log(call.message, answer)

    data = call.data
    user = db.get_userinfo(0, call.message.chat.id)
    call_id = call.message.chat.id

    if data == "M-add":
        bot.send_message(call.message.chat.id, "<b>Введите номер телефона клиента в формате: 89012345678.</b>",
                         parse_mode='HTML',
                         reply_markup=back())  # TODO убрать тел из user_id и добавить возможность посл привязки
        bot.register_next_step_handler(call.message, InputPhone)

    elif data.startswith("search_"):
        if data == "search_phone":
            bot.send_message(call_id, "Введите номер телефона клиента:", reply_markup=m.C_back())
            bot.register_next_step_handler(call.message, SearchPhone)
        if data == "search_name":
            pass
        if data == "search_tg":
            pass
        if data == "search_list":
            pass

    elif data.startswith('S-'):
        if data == "S-info":
            bot.send_message(call.message.chat.id,
                             "Имя: {}, Фамилия: {}, Номер телефона: {}, \nСтатус: {}".format(user.user_Rname,
                                                                                             user.user_Rlname,
                                                                                             user.phone, user.Rank))
        if data == "S-name":
            if user.Rank == "MASTER" or user.Rank == "ADMIN":
                db.set_comment("S", user.user_id)
            bot.send_message(call.message.chat.id,
                             "Введите ваше имя.",
                             reply_markup=m.S_back())
            bot.register_next_step_handler(call.message, InputName)

        if data == "S-lname":
            if user.Rank == "MASTER" or user.Rank == "ADMIN":
                db.set_comment("S", user.user_id)
            bot.send_message(call.message.chat.id,
                             "Введите вашу фамилию",
                             reply_markup=m.S_back())
            bot.register_next_step_handler(call.message, InputLastName)

        if data == "S-phone":
            if user.Rank == "MASTER" or user.Rank == "ADMIN":
                db.set_comment("S", user.user_id)
            bot.send_message(call.message.chat.id,
                             "Введите ваш номер телефона. Например:  +79031234567 или 9031234567.",
                             reply_markup=m.S_back())
            bot.register_next_step_handler(call.message, InputPhone)

    elif data.startswith('back_'):
        if data == "back_to_menu":
            bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
            return handle_message1(call.message)
        if data == "back_to_setting":
            bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
            return handle_message3(call.message)
        if data == "back_to_search":
            bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
            return c.create_search_list(call.message)

    else:
        inline.inline_main_func(call)


""" 
______________________________________________________________________________________________________
______________________________________________________________________________________________________
______________________________________________________________________________________________________
MASTER_____MASTER_____MASTER_____MASTER_____MASTER_____MASTER_____MASTER_____MASTER_____
"""


# TODO доделать меню записей, выполненые сеансы, отправку уведомений (начало, отмена, напоминания за час)
# TODO почистить код от мусора, сделать меню клиентов, справочник, старые записи, акции, масс рассылку
# TODO сделать пометки о прошедших днях


def SearchPhone(message):
    print(message)
    # TODO тутутутутуутутутуттутут
    pass


def InputPhone(message):
    try:
        phone = c.CheckPhone(message)
        print('Телефон 205 - {}'.format(phone))

        if phone is False:
            bot.register_next_step_handler(message, InputPhone)
            return

        user = db.get_userinfo(0, message.chat.id)

        if (user.Rank == "MASTER" or user.Rank == "ADMIN") and user.comment != "S":
            user2 = db.get_userinfo(1, phone)
            if user2 is None:
                db.new_user_phone(phone)
                db.setRank('U', phone)
                db.buffer(message.chat.id, phone)
                bot.send_message(message.chat.id, "Клиент не найден. Введите имя нового клиента.", reply_markup=back())
                bot.register_next_step_handler(message, InputName)

            else:
                text = "ФИО - {} {}, \nТелефон - {}, Telegram - {}".format(user2.user_Rname,
                                                                           user2.user_Rlname,
                                                                           user2.phone,
                                                                           user2.username)
                bot.send_message(message.chat.id, text=text)
                db.buffer(message.chat.id, user2.user_id)
                keytab = func.note_seance(now.year, now.month, now.day)
                bot.send_message(message.chat.id, "Выберите удобную дату для записи. "
                                                  "Галочками отмечены свободные половины дня "
                                                  "[День(~12:00)/Вечер(~17:00)].", reply_markup=keytab)
        else:
            phones = db.get_all_phones()
            for x in phones:
                if phone == x:
                    bot.send_message(user.user_id, "Такой номер уже существует, введите другой номер:",
                                     reply_markup=m.S_back())
                    bot.register_next_step_handler(message, InputPhone)
                    return

            db.set_phone(phone, user.user_id)
            db.set_comment(None, user.user_id)
            bot.send_message(user.user_id, "Ваш номер успешно сохранен.",
                             reply_markup=m.make_markup_menu(user.Rank))

    except Exception as e:
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        print("Error phone input ", e)
        # TODO ERROR LOG


def InputName(message):
    try:
        if not message.text.isalpha() or len(message.text) < 2:
            bot.send_message(message.chat.id, "Ничего не введено, или введены недопустимые символы.")
            bot.register_next_step_handler(message, InputName)
            return

        user = db.get_userinfo(0, message.chat.id)

        if (user.Rank == "MASTER" or user.Rank == "ADMIN") and user.comment != "S":
            db.set_user_rname(message.text, user.note_id)
            bot.send_message(user.user_id, "Имя сохранено, введите фаммилию:")
            bot.register_next_step_handler(message, InputLastName)
            return
        else:
            db.set_user_rname(message.text, message.chat.id)

            if user.Rank == "R":
                bot.send_message(user.user_id, "Имя сохранено, введите фаммилию:")
                bot.register_next_step_handler(message, InputLastName)
                return
            else:
                db.set_comment(None, user.user_id)
                bot.send_message(user.user_id, "Имя сохранено", reply_markup=m.make_markup_menu(user.Rank))

    except Exception as e:
        print("Error name input ", e)


def InputLastName(message):
    try:
        if not message.text.isalpha() or len(message.text) < 2:
            bot.send_message(message.chat.id, "Ничего не введено, или введены недопустимые символы.")
            bot.register_next_step_handler(message, InputLastName)
            return

        user = db.get_userinfo(0, message.chat.id)

        if (user.Rank == "MASTER" or user.Rank == "ADMIN") and user.comment != "S":
            db.set_user_rlname(message.text, user.note_id)
            bot.send_message(user.user_id, "Клиент добавлени в список клиентов.")
            keytab = func.note_seance(now.year, now.month, now.day)
            bot.send_message(message.chat.id, "Выберите удобную дату для записи. "
                                              "Галочками отмечены свободные половины дня "
                                              "[День(~12:00)/Вечер(~17:00)].", reply_markup=keytab)
        else:
            db.set_user_rlname(message.text, message.chat.id)
            if user.Rank == "R":
                db.setRank('U', user.user_id)
                markup = m.make_markup_menu('U')
                bot.send_message(user.user_id,
                                 "Фамилия сохарнена.\nТеперь вы можете записаться на сеанс к мастеру.",
                                 reply_markup=markup)
                handle_message1(message)
            else:
                db.set_comment(None, user.user_id)
                markup = m.make_markup_menu(user.Rank)
                bot.send_message(user.user_id, "Фамилия сохарнена.", reply_markup=markup)

    except Exception as e:
        print("Error name input ", e)


bot.infinity_polling(True)
