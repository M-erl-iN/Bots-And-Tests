from auth import TOKEN
from telegram import ReplyKeyboardMarkup
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)


def first_placed(update, context):
    reply_keyboard = [["/2"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!\n\n"
        "Далее вы можете пройти в зал 2, где представлены скелеты динозавров.",
        reply_markup=markup,
    )
    return 1


def second_placed(update, context):
    reply_keyboard = [["/3"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "В данном зале представлены скелеты динозавров.\n\n"
        "Далее вы можете пройти в зал 3, где представлены интересные "
        "археологические находки.",
        reply_markup=markup,
    )
    return 2


def third_placed(update, context):
    reply_keyboard = [["/4", "/1"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "В данном зале представлены интересные археологические находки.\n\n"
        "Далее вы можете пройти в зал 4, где представлены "
        "произведения искусства или снова пройти в зал 1, "
        "чтобы выйти или пройти музей снова",
        reply_markup=markup,
    )
    return 3


def fourth_placed(update, context):
    reply_keyboard = [["/1"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "В данном зале представлены произведения искусства.\n\n"
        "Далее вы можете пройти в зал 1, чтобы снова обойти наш музей, "
        "или выйти",
        reply_markup=markup,
    )
    return 4


def again_first_placed(update, context):
    reply_keyboard = [["/2", "/exit"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Снова Добро пожаловать! Вы можете еще раз пройти музей или же выйти.",
        reply_markup=markup,
    )
    return 5


def exit_from_museum(update, context):
    update.message.reply_text(
        "Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!"
    )
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", first_placed)],
        states={
            1: [CommandHandler("2", second_placed)],
            2: [CommandHandler("3", third_placed)],
            3: [
                CommandHandler("4", fourth_placed),
                CommandHandler("1", again_first_placed),
            ],
            4: [CommandHandler("1", again_first_placed)],
            5: [
                CommandHandler("exit", exit_from_museum),
                CommandHandler("2", second_placed),
            ],
        },
        fallbacks=[CommandHandler("exit", exit_from_museum)],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == "__main__":
    main()
