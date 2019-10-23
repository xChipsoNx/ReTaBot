import calendar
import datetime

import telebot
from telebot import types

import APIconst
from dbhelper import DBHelper

db = DBHelper()
bot = telebot.TeleBot(APIconst.API_TOKEN)
now = datetime.datetime.now()

def create_callback_data(action, year, month, day):
    """ Create the callback data associated to each button"""
    return ";".join([action, str(year), str(month), str(day)])


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")

def create_text(year, month, day):
    try:
        w = db.get_work(datetime.date(year, month, day))
        try:
            if w[0] == 1:
                if day < now.day and month == now.month:
                    text = str(day) + "🆗"
                else:
                    text = str(day) + "✅"
            else:
                if day < now.day and month == now.month:
                    text = str(day) + "⏺"
                else:
                    text = str(day) + "❌"
        except IndexError as e:
            return str(day)

        return text
    except TypeError:
        print("TypeError")


def create_calendar(year=None, month=None, dday=None):
    """
    Create an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """

    if year == None: year = now.year
    if month == None: month = now.month
    data_ignore = create_callback_data("DAY-IGNORE", year, month, 0)
    keytab = types.InlineKeyboardMarkup(row_width=7)

    keyboard = []

    # First row - Month and Year
    row = []
    text = calendar.month_name[month] + " " + str(year)
    callback_data = data_ignore
    row.append(telebot.types.InlineKeyboardButton(text=text,
                                                  callback_data=callback_data))
    keyboard.append(row)
    keytab.add(*row)

    # Second row - Week Days
    row = []
    for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        row.append(telebot.types.InlineKeyboardButton(text=day,
                                                      callback_data=data_ignore))
    keyboard.append(row)
    keytab.add(*row)
    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []

        for day in week:
            if day == 0:
                callback_data = data_ignore
                row.append(telebot.types.InlineKeyboardButton(text=" ",
                                                              callback_data=callback_data))
            else:
                text = create_text(year, month, day)

                if day < now.day and month == now.month:
                    callback_data = data_ignore
                else:
                    callback_data = create_callback_data("DAY", year, month, day)

                row.append(telebot.types.InlineKeyboardButton(text=text,
                                                              callback_data=callback_data))
        keyboard.append(row)
        keytab.add(*row)

    # Last row - Buttons
    row = []
    callback_data = create_callback_data("DAY-PREV-MONTH", year, month, day)
    row.append(telebot.types.InlineKeyboardButton(text="<",
                                                  callback_data=callback_data))
    callback_data = data_ignore
    row.append(telebot.types.InlineKeyboardButton(text=" ",
                                                  callback_data=callback_data))
    callback_data = create_callback_data("DAY-NEXT-MONTH", year, month, day)
    row.append(telebot.types.InlineKeyboardButton(text=">",
                                                  callback_data=callback_data))
    keyboard.append(row)
    keytab.add(*row)

    return keytab


def process_calendar_selection(query):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    :param telegram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param telegram.Update update: The update, as provided by the CallbackQueryHandler
    :return: Returns a tuple (Boolean,datetime.datetime), indicating if a date is selected
                and returning the date if so.
    """

    ret_data = (False, None)
    (action, year, month, day) = separate_callback_data(query.data)
    curr = datetime.datetime(int(year), int(month), 1)

    if action == "DAY-IGNORE":
        bot.answer_callback_query(callback_query_id=query.id)

    elif action == "DAY":

        bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat.id,
                              message_id=query.message.message_id)

        ret_data = True, datetime.date(int(year), int(month), int(day))

    elif action == "DAY-PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        markup = create_calendar(int(pre.year), int(pre.month))
        bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat.id,
                              message_id=query.message.message_id,
                              reply_markup=markup)
        ret_data = False, 'prev'

    elif action == "DAY-NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        markup = create_calendar(int(ne.year), int(ne.month))
        bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat.id,
                              message_id=query.message.message_id,
                              reply_markup=markup)
        ret_data = False, 'next'
    else:
        bot.answer_callback_query(callback_query_id=query.id, text="Something went wrong!")
        # UNKNOWN
    return ret_data
