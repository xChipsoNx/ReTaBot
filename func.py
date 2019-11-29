from APIconst import API_TOKEN
from mycalendar import *

bot = telebot.TeleBot(API_TOKEN)


def note_seance(year, month, nday):
    this_month = calendar.monthcalendar(year, month)
    keylist = []
    for week in this_month:
        for day in week:
            if day != 0 and day >= nday:
                w = db.get_work(datetime.date(year, month, day))
                if w[0] == 1:
                    h = db.get_halfs(datetime.date(year, month, day))
                    callback_data = create_callback_data("WDAY", year, month, day)
                    if (h[0] is None or h[0] == 0) and (h[1] is None or h[1] == 0):
                        text = str(day) + '.' + str(month) + '.' + str(year) + " [✅/✅]"
                        keylist.append(telebot.types.InlineKeyboardButton(text=text,
                                                                          callback_data=callback_data))
                    elif h[0] is None or h[0] == 0:
                        text = str(day) + '.' + str(month) + '.' + str(year) + " [✅/❌]"
                        keylist.append(telebot.types.InlineKeyboardButton(text=text,
                                                                          callback_data=callback_data))
                    elif h[1] is None or h[1] == 0:
                        text = str(day) + '.' + str(month) + '.' + str(year) + " [❌/✅]"
                        keylist.append(telebot.types.InlineKeyboardButton(text=text,
                                                                          callback_data=callback_data))
    return keylist


def show_half_u(date):
    keytab = types.InlineKeyboardMarkup()
    (action, year, month, day) = date.split(";")
    year = int(year)
    month = int(month)
    day = int(day)
    h = db.get_halfs(datetime.date(year, month, day))
    print(h)
    if h[0] is None or h[0] == 0:
        callback_data = create_callback_data("HALF-1", year, month, day)
        text = "Пр. время начала сеанса 14:00 " + "[✅]"
        keytab.add(telebot.types.InlineKeyboardButton(text=text,
                                                      callback_data=callback_data))

    if h[1] is None or h[1] == 0:
        callback_data = create_callback_data("HALF-2", year, month, day)
        text = "Пр. время начала сеанса 18:00 " + "[✅]"
        keytab.add(telebot.types.InlineKeyboardButton(text=text,
                                                      callback_data=callback_data))
    return keytab


def make_note(call, h):
    # TODO уведомления о записях
    user = db.get_userinfo(0, call.message.chat.id)
    (action, year, month, day) = call.data.split(";")
    note_id = str(year) + '-' + str(month) + '-' + str(day) + "-" + str(h)
    if user.Rank == "MASTER" or user.Rank == "ADMIN":
        db.make_note(datetime.date(int(year), int(month), int(day)), h, user.note_id, note_id)
        db.remove_buf(user.user_id)
    else:
        try:
            db.make_note(datetime.date(int(year), int(month), int(day)), h, call.message.chat.id, note_id)
            masters = db.get_all_masters()

            nTime = '~14-00'
            if h == 2:
                nTime = '~18-00'

            for master in masters:
                bot.send_message(master, "✅ К вам записался клиент {} {}, тел: {}, tg: @{}\nна {}/{}/{} в {}."
                                 .format(user.user_Rname, user.user_Rlname, user.phone, user.username,
                                         day, month, year, nTime))

                # TODO  доделать систему, доделать кнопку " и "добавить коментарий"

        except Exception as e:
            print("Error make note ", e)


def note_parse(user):
    try:
        (year, month, day, h) = user.note_id.split("-")
        return datetime.date(int(year), int(month), int(day)), int(h)
    except AttributeError:
        print("Error note parse")


def cancel_note(call):
    try:
        user = db.get_userinfo(0, call.message.chat.id)
        (date, h) = note_parse(user)
        db.remove_note(date, h, call.message.chat.id)
        anskey = types.InlineKeyboardMarkup(row_width=2)
        note = types.InlineKeyboardButton(text="Записаться на сеанс.", callback_data="U-add")
        past = types.InlineKeyboardButton(text="Решить позже.", callback_data="U-past")
        anskey.add(note, past)
        return anskey
    except TypeError:
        print("Error cancel note")


def date_handler(call):  # TODO доделать показ месяцев
    try:

        selected, date = process_calendar_selection(call)

        if selected:
            work = db.get_work(date)

            if work[0] is None:
                work = 1
                db.update_work(work, date)
            else:
                work = None
                db.update_work(work, date)

            markup = create_calendar(date.year, date.month, date.day)
            bot.edit_message_text(text="Вы выбрали: {}".format(date),
                                  chat_id=call.message.chat.id,
                                  reply_markup=markup,
                                  message_id=call.message.message_id)
    except IndexError as e:
        print(e)


def mshow_notes(year, month, nday):
    keytab = types.InlineKeyboardMarkup()
    my_calendar = calendar.monthcalendar(year, month)
    time1 = ' 🌞14:00 👀'
    time2 = ' 🌙18:00 👀'
    for week in my_calendar:
        for day in week:
            if day != 0 and day >= nday:
                w = db.get_work(datetime.date(year, month, day))
                if w[0] == 1:
                    h = db.get_halfs(datetime.date(year, month, day))
                    user1 = db.get_userinfo(0, h[0])
                    user2 = db.get_userinfo(0, h[1])
                    if h[0] is not None:
                        callback_data = "NOTE-" + str(h[0])
                        text = "{}-{}-{} ".format(day, month, year) + time1 + ' ' + user1.user_Rname
                        keytab.add(types.InlineKeyboardButton(text=text,
                                                              callback_data=callback_data))

                    if h[1] is not None:
                        callback_data = "NOTE-" + str(h[1])
                        text = "{}-{}-{} ".format(day, month, year) + time2 + ' ' + user2.user_Rname
                        keytab.add(types.InlineKeyboardButton(text=text,
                                                              callback_data=callback_data))
    return keytab


def note_detal_info(call):
    keytab = types.InlineKeyboardMarkup()
    CD, ID = call.data.split('-')
    user = db.get_userinfo(0, ID)
    callback = 'M-rem-' + str(user.user_id) + '-' + str(user.note_id)
    print(callback)
    text = "ФИО - {} {}, \nТелефон - {}, Telegram - @{}".format(user.user_Rname,user.user_Rlname,
                                                                user.phone, user.username)
    keytab.add(types.InlineKeyboardButton(text="❌ Удалить запись.",
                                          callback_data=callback))
    keytab.add(types.InlineKeyboardButton(text="Назад.",
                                          callback_data='M-SNS-B'))
    # TODO доделать кнопку "Выполнено", добавить архив работ, кнопку "Напомнить"

    return str(text), keytab


def remote_note(call):
    user = db.get_userinfo(0, call.message.chat.id)
    (date, h) = note_parse(user.note_id)
    db.remove_note(date, h, call.message.chat.id)


def log(message, answer):
    print("\n -------")  # ведение лга в терминал
    print(datetime.datetime.now())
    print("Сообщение от {0} {1}. (id = {2})) \n Текст - {3}".format(message.from_user.first_name,
                                                                    message.from_user.last_name,
                                                                    str(message.from_user.id),
                                                                    message.text))
    print(answer)


"_INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE_"
"_INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE__INLINE_"
