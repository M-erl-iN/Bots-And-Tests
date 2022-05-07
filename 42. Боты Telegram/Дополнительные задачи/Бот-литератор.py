from auth import TOKEN
from telegram import ReplyKeyboardMarkup
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)

verse = """Травка зеленеет
Солнышко блестит
Ласточка с весною
В сени к нам летит
С нею солнце краше
И весна милей
Прощебечь с дороги
Нам привет скорей
Дам тебе я зерен
А ты песню спой
Что из стран далеких
Принесла с собой""".split(
    "\n"
)


def start(update, context):
    verse_str = verse[0]
    update.message.reply_text(verse_str)
    return 1


def get_str(update, context):
    text = update.message.text
    try:
        if not context.user_data:
            context.user_data["all_str"] = [verse[0], text]
        else:
            context.user_data["all_str"].append(text)
        current_corr_str = verse[len(context.user_data["all_str"]) - 1]
        if current_corr_str == text:
            send_str = verse[len(context.user_data["all_str"])]
            update.message.reply_text(send_str)
            if send_str == verse[-1]:
                raise IndexError
            context.user_data["all_str"].append(current_corr_str)
            if context.user_data["all_str"] == verse:
                raise IndexError
            return 1
        else:
            update.message.reply_text("нет, не так")
            update.message.reply_text(
                f"Подсказка, правильная строка: {current_corr_str}"
            )
            del context.user_data["all_str"][-1]
            return 1
    except IndexError:
        update.message.reply_text("Ты прекрасно справился! Может повторим?")
        return ConversationHandler.END


def stop(update, context):
    update.message.reply_text("Попробуй еще раз, у тебя точно получится!")


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            1: [
                CommandHandler("stop", stop),
                MessageHandler(Filters.text, get_str, pass_user_data=True),
            ],
        },
        fallbacks=[CommandHandler("stop", stop)],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == "__main__":
    main()
