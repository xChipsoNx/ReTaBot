from func import *


def make_settings_keyboard():
    settings = types.InlineKeyboardMarkup(row_width=1)
    but_info = types.InlineKeyboardButton("Мои данные.", callback_data="S-info")
    but_set1 = types.InlineKeyboardButton("Изменить имя.", callback_data="S-name")
    but_set2 = types.InlineKeyboardButton("Изменить фамилию.", callback_data="S-lname")
    but_set3 = types.InlineKeyboardButton("Изменить номер телефона.", callback_data="S-phone")
    settings.add(but_info, but_set1, but_set2, but_set3)
    return settings


def make_markup_menu(rank):
    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # разметка главного кнопочного меню
    markup_menuAdmin = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    Rmarkup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    Mmarkup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_reviews = types.KeyboardButton('💎Работы мастера')
    btn_note = types.KeyboardButton('📆Запись')  # главное кнопочное меню - кнопки
    btn_help = types.KeyboardButton('✉Написать мастеру')
    btn_settings = types.KeyboardButton('⚙Настройки')
    btn_userlist = types.KeyboardButton('👬Клиенты')
    btn_reg = types.KeyboardButton('🚀Регистрация', request_contact=True)
    markup_menu.add(btn_note, btn_help, btn_reviews, btn_settings)
    markup_menuAdmin.add(btn_reg, btn_help, btn_note, btn_userlist, btn_reviews, btn_settings)
    Rmarkup.add(btn_reg, btn_reviews)
    Mmarkup.add(btn_note, btn_userlist, btn_reviews, btn_settings)

    if rank == "R":
        return Rmarkup
    elif rank == "U":
        return markup_menu
    elif rank == "MASTER":
        return Mmarkup
    else:
        return markup_menuAdmin


def back():
    mback = types.InlineKeyboardMarkup()
    mback.add(types.InlineKeyboardButton("Назад.", callback_data="back_to_menu"))
    return mback


def S_back():
    sback = types.InlineKeyboardMarkup()
    sback.add(types.InlineKeyboardButton("Назад.", callback_data="back_to_setting"))
    return sback


def C_back():
    cback = types.InlineKeyboardMarkup()
    cback.add(types.InlineKeyboardButton("Назад.", callback_data="back_to_search"))
    return cback


def admin_panel():
    adminRank = types.InlineKeyboardMarkup()
    adminRank.add(types.InlineKeyboardButton("Сменить себе ранк.", callback_data="admin_change_rank"))
    return adminRank


def admin_ranks():
    okrank = types.InlineKeyboardMarkup(row_width=2)
    rank0 = types.InlineKeyboardButton(text="User", callback_data="admin_to_user")
    rankA = types.InlineKeyboardButton(text="Admin", callback_data="admin_to_admin")
    rankM = types.InlineKeyboardButton(text="Master", callback_data="admin_to_master")
    rankR = types.InlineKeyboardButton(text="New User", callback_data="admin_to_reg")
    okrank.add(rank0, rankA, rankM, rankR)
    return okrank


def main_note_menu(message):
    keyNote = types.InlineKeyboardMarkup(row_width=1)
    but_AddNote = types.InlineKeyboardButton(text="Записаться на сеанс.", callback_data="U-add")
    but_work = types.InlineKeyboardButton(text="Назначить рабочие дни.", callback_data="M-work")
    but_AddNoteM = types.InlineKeyboardButton(text="Добавить запись.", callback_data="M-add")  # для мастера
    but_RemNote = types.InlineKeyboardButton(text="Отменить запись.",
                                             callback_data="U-rem")  # для тех у кого есть запись < 24ч
    but_ShowNotes = types.InlineKeyboardButton(text="Показать записи.",
                                               callback_data="M-SNS")  # для мастера, список на 1-3-5-7-10дней
    try:
        user = db.get_userinfo(0, message.chat.id)
        print(user.note_id, user.Rank)

        if user.Rank == "MASTER":
            keyNote.add(but_ShowNotes, but_AddNoteM, but_work)

        elif user.Rank == "ADMIN":
            keyNote.add(but_AddNote, but_ShowNotes, but_AddNoteM, but_work, but_RemNote)

        elif (user.note_id is None) and (user.Rank == "U"):
            keyNote.add(but_AddNote)

        elif (user.note_id is not None) and (user.Rank == "U"):
            (date, h) = note_parse(user)
            text = "<b>Есть запись.</b>"
            if h == 1:
                text = "<b>Вы записаны {} на день ~~12:00.</b>".format(date)
            if h == 2:
                text = "<b>Вы записаны {} на вечер ~~17:00.</b>".format(date)
            bot.send_message(message.chat.id, text, parse_mode='HTML')
            keyNote.add(but_RemNote)

        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyNote)
    except AttributeError:
        bot.send_message(message.chat.id,
                         "Возникли проблемы с вашими данными. Введите /start.\n Если это не поможет, напишите "
                         "администратору: @Alex_Chipson")