from auth import TOKEN
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)


def start(update, context):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "Или пропустить вопрос, послав команду /skip.\n"
        "В каком городе вы живёте?"
    )

    return 1


def first_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    locality = update.message.text
    update.message.reply_text("Какая погода в городе {locality}?".format(**locals()))
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 2


def second_response(update, context):
    # Ответ на второй вопрос.
    # Мы можем его сохранить в базе данных или переслать куда-либо.
    weather = update.message.text
    update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END  # Константа, означающая конец диалога.
    # Все обработчики из states и fallbacks становятся неактивными.


def skip_first_response(update, context):
    update.message.reply_text("Какая погода у вас за окном?")
    return 2


def stop(update, context):
    update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            1: [
                CommandHandler("stop", stop),
                CommandHandler("skip", skip_first_response),
                MessageHandler(Filters.text, first_response),
            ],
            2: [MessageHandler(Filters.text, second_response)],
        },
        fallbacks=[CommandHandler("stop", stop)],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == "__main__":
    main()
