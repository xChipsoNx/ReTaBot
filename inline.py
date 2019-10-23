from markups import *
import client as c
import func


def inline_main_func(call):
    data = call.data
    user = db.get_userinfo(0, call.message.chat.id)

    if data.startswith('U-'):
        if data == "U-add":
            if user.note_id is None:

                keytab = note_seance(now.year, now.month, now.day)
                bot.send_message(call.message.chat.id, "Выберите удобную дату для записи. "
                                                       "Галочками отмечены свободные половины дня "
                                                       "[День(~12:00)/Вечер(~17:00)].", reply_markup=keytab)
            else:
                bot.send_message(call.message.chat.id, "Вы уже записаны.")
        if data == "U-rem":
            if user.note_id is None:
                bot.send_message(call.message.chat.id, "У вас нет записей.")
            else:
                anskey = cancel_note(call)
                bot.send_message(call.message.chat.id,
                                 "Вы отменили свою запись. Запишитесь на новое время, или решите позже?",
                                 reply_markup=anskey)

        if data == "U-past":
            bot.send_message(call.message.chat.id, "<b>Тогда буду ждать вашего решения! Удачи!</b>",
                             reply_markup=make_markup_menu(user.Rank),
                             parse_mode='HTML')

    elif data.startswith('M-'):
        if data == "M-SNS":
            markups = mshow_notes(now.year, now.month, now.day)
            bot.send_message(call.message.chat.id, "<b>Ближайшие записи.</b>", parse_mode='HTML', reply_markup=markups)

        if data == "M-SNS-B":
            markups = mshow_notes(now.year, now.month, now.day)
            bot.edit_message_text(chat_id=call.message.chat.id, text="<b>Ближайшие записи.</b>",
                                  parse_mode='HTML', reply_markup=markups,
                                  message_id=call.message.message_id)

        if data == "M-work":
            markup = create_calendar(now.year, now.month)
            bot.send_message(call.message.chat.id, "Пожалуйста, выберите дату", reply_markup=markup)

        if data.startswith('M-rem-'):
            try:
                M, rem, id, year, month, day, half = call.data.split("-")
                db.remove_note(datetime.date(int(year), int(month), int(day)), int(half), int(id))
            except ValueError:
                bot.answer_callback_query(call.id, text="Ошибка, проблемы с записью.")

            else:
                bot.send_message(call.message.chat.id, "Запись удалена.")
                markups = mshow_notes(now.year, now.month, now.day)
                bot.edit_message_text(chat_id=call.message.chat.id, text="<b>Ближайшие записи.</b>",
                                      parse_mode='HTML', reply_markup=markups,
                                      message_id=call.message.message_id)

    elif data.startswith('client_'):
        if data == "client_list":
            c.create_search_list(call.message)
        if data == "client_archive":
            pass
        if data == "client_add":
            keytab = func.note_seance(now.year, now.month, now.day)
            bot.send_message(call.message.chat.id, "Выберите удобную дату для записи. "
                                                   "Галочками отмечены свободные половины дня "
                                                   "[День(~12:00)/Вечер(~17:00)].", reply_markup=keytab)

    elif data.startswith('NOTE-'):
        text, markupn = note_detal_info(call)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=text,
                              reply_markup=markupn,
                              message_id=call.message.message_id)

    elif data.startswith('DAY'):
        date_handler(call)

    elif data.startswith('WDAY'):
        keytab = show_half_u(call.data)
        (action, year, month, day) = call.data.split(";")
        bot.edit_message_text(text="Вы выбрали: {}/{}/{}\nВыберите время:".format(day, month, year),
                              chat_id=call.message.chat.id,
                              reply_markup=keytab,
                              message_id=call.message.message_id)

    elif data.startswith('HALF-'):
        user = db.get_userinfo(0, call.message.chat.id)
        print(call.data)
        if data.startswith('HALF-1'):
            make_note(call, 1)
            if user.Rank != ("MASTER" or "ADMIN"):
                (action, year, month, day) = call.data.split(";")
                bot.edit_message_text(text="Вы записались к мастеру на {}/{}/{} в ~12:00\n"
                                           "Напишите мастеру и обговорите детали встречи.".format(day, month, year),
                                      chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)
            else:
                (action, year, month, day) = call.data.split(";")
                bot.edit_message_text(text="Вы записали клиента на {}/{}/{} в ~12:00\n"
                                           "Напишите клиенту и сообщите ему о записи.".format(day, month, year),
                                      chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)

        if data.startswith('HALF-2'):
            make_note(call, 2)
            if user.Rank != ("MASTER" or "ADMIN"):
                (action, year, month, day) = call.data.split(";")
                bot.edit_message_text(text="Вы записались к мастеру на {}/{}/{} в ~17:00\n"
                                           "Напишите мастеру и обговорите детали встречи.".format(day, month, year),
                                      chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)
            else:
                (action, year, month, day) = call.data.split(";")
                bot.edit_message_text(text="Вы записали клиента на {}/{}/{} в ~17:00\n"
                                           "Напишите клиенту и сообщите ему о записи.".format(day, month, year),
                                      chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)

    elif data.startswith('admin_'):

        admin = db.get_userinfo(0, call.message.chat.id)

        if data == 'admin_change_rank':
            panel = admin_ranks()
            bot.send_message(admin.user_id, "Выберайте:", reply_markup=panel)

        if data.startswith('admin_to_'):
            if data == "admin_to_user":
                db.setRank('U', call.message.chat.id)
            if data == "admin_to_admin":
                db.setRank("ADMIN", call.message.chat.id)
            if data == "admin_to_master":
                db.setRank("MASTER", call.message.chat.id)
            if data == "admin_to_reg":
                db.setRank("R", call.message.chat.id)

    else:
        bot.answer_callback_query(call.id, text="Error callback")
