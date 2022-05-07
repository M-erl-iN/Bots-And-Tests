import time

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater


def help(update, context):
    update.message.reply_text("Я пока не умею помогать...")


def start(update, context):
    reply_keyboard = [["/time", "/date"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Я бот-даты и времени.", reply_markup=markup)


def current_time(update, context):
    current_time_message = time.strftime("Время %H:%M", time.localtime())
    update.message.reply_text(current_time_message)


def current_date(update, context):
    current_time_message = time.strftime("Дата %d-%m-%Y", time.localtime())
    update.message.reply_text(current_time_message)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("time", current_time))
    dp.add_handler(CommandHandler("date", current_date))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    updater.start_polling()
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == "__main__":
    main()
