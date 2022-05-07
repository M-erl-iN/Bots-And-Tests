from auth import TOKEN
from deep_translator import GoogleTranslator
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

# pip install deep-translator
# Бот автоматические определяет на какой язык переводить


def start(update, context):
    text = (
        "Привет! Я бот-переводчик, я могу переводить с русского на английский и наоборот, "
        "просто введите любое слово, я сам пойму на какой из языков переводить."
    )
    update.message.reply_text(text)


def translate(update, context):
    text = update.message.text
    count_en = count_ru = 0
    for i in text:
        if i.lower() in "qwertyuiopasdfghjklzxcvbnm":
            count_en += 1
        elif i.lower() in "йцукенгшщзхъфывапролджэячсмитьбю":
            count_ru += 1
    if count_en > count_ru:
        source = "en"
        target = "ru"
    else:
        source = "ru"
        target = "en"
    translated = GoogleTranslator(source=source, target=target).translate(text)
    update.message.reply_text(translated)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, translate))

    updater.start_polling()
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == "__main__":
    main()
