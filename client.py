from telebot import types

from func import bot, db


# from markups import back


def create_client_menu(message):
    client_menu = types.InlineKeyboardMarkup()
    but1 = types.InlineKeyboardButton(text="Справочник клиентов.", callback_data="client_list")
    but2 = types.InlineKeyboardButton(text="Архив записей.", callback_data="client_archive")
    client_menu.add(but1, but2)
    bot.send_message(message.chat.id, "Выберите действие: ", reply_markup=client_menu)


def create_search_list(message):
    client_list = types.InlineKeyboardMarkup(row_width=1)
    but1 = types.InlineKeyboardButton(text="Номер телефона.", callback_data="search_phone")
    but2 = types.InlineKeyboardButton(text="Имя, или хотя бы первые 3 буквы имени.", callback_data="search_name")
    but3 = types.InlineKeyboardButton(text="Telegram никнейм.", callback_data="search_tg")
    but4 = types.InlineKeyboardButton(text="Список.", callback_data="search_list")
    client_list.add(but1, but2, but3, but4)
    bot.send_message(message.chat.id, "Как будете искать клиентов?", reply_markup=client_list)


def create_about_client():
    about_client = types.InlineKeyboardMarkup(row_width=1)
    but1 = types.InlineKeyboardButton(text="Записать на сеанс.", callback_data="client_add")
    but2 = types.InlineKeyboardButton(text="Показать архив.", callback_data="client_show_archive")
    but3 = types.InlineKeyboardButton(text="Назад.", callback_data="back_to_search")
    about_client.add(but1, but2, but3)
    return about_client


def CheckPhone(message):
    text = message.text
    print('Телефон 25 - {}'.format(text))

    if not text[1:].isdigit():
        bot.send_message(message.chat.id, "Номер может состоять из цифр и знака '+'.")
        return False

    if len(text) < 10:
        bot.send_message(message.chat.id,
                         "Номер слишком короткий номер.")
        return False
    else:
        phone = PhoneRefactor(str(text))
        if phone is not False:
            return phone
        else:
            bot.send_message(message.chat.id, "Номер должен начинаться с (+79/89/9).")
            return False


def PhoneRefactor(phone):

    if phone.startswith('+79'):
        return phone
    elif len(phone) == 10 and phone[0] == '9':
        return '+7' + phone
    elif len(phone) == 11 and (phone.startswith('89') or phone.startswith('79')):
        return '+7' + phone[1:]
    else:
        return False


def search_with_phone(message):
    phone = message.text

    phones = db.get_all_phones()
    for x in phones:
        if phone == x:
            user = db.get_userinfo(1, phone)
            text = "ФИО - {} {}, \nТелефон - {}, Telegram - @{}".format(user.user_Rname, user.user_Rlname,
                                                                        user.phone, user.username)
            markup = create_about_client()
            db.buffer(message.chat.id, user.user_id)
            bot.send_message(message.chat.id, text=text, reply_markup=markup)


def search_with_name(message):
    name = message.text
    names = db.get_all_names()
    markup = types.InlineKeyboardMarkup(row_width=1)
    for x in names:
        if name == x:
            text = ""
            callback = ""
            markup.add(types.InlineKeyboardButton(text=text, callback_data=callback))



