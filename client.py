from telebot import types
from func import bot
from markups import back


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


def CheckPhone(message):
    text = message.text
    print('Телефон 25 - {}'.format(text))

    if not text[1:].isdigit():
        bot.send_message(message.chat.id, "Номер может состоять из цифр и знака '+'.", reply_markup=back())
        return False

    if len(text) < 10:
        bot.send_message(message.chat.id,
                         "Номер слишком короткий номер.",
                         reply_markup=back())
        return False
    else:
        phone = PhoneRefactor(str(text))
        if phone is not False:
            return phone
        else:
            bot.send_message(message.chat.id, "Номер должен начинаться с (+79/89/9).", reply_markup=back())
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





