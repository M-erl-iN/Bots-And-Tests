import random

from telegram import ReplyKeyboardMarkup
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)


def help(update, context):
    update.message.reply_text("Я пока не умею помогать...")


def start(update, context):
    reply_keyboard = [["/dice", "/timer"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Начальное меню", reply_markup=markup)


def dice(update, context):
    reply_keyboard = [
        ["Кинуть 1 шестигранный кубик", "Кинуть 2 шестигранных кубика одновременно"],
        ["Кинуть 20-гранный кубик", "вернуться назад"],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Подкинь кубик", reply_markup=markup)


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


# Обычный обработчик, как и те, которыми мы пользовались раньше.
def set_timer(update, context):
    """Добавляем задачу в очередь"""
    text = update.message.text
    if text == "Кинуть 1 шестигранный кубик":
        update.message.reply_text(f"Выпало число: {random.randint(1, 6)}")
    elif text == "Кинуть 2 шестигранных кубика одновременно":
        update.message.reply_text(
            f"Выпали числа: {random.randint(1, 6)} и {random.randint(1, 6)}"
        )
    elif text == "Кинуть 20-гранный кубик":
        update.message.reply_text(f"Выпало число: {random.randint(1, 20)}")
    elif text == "вернуться назад":
        reply_keyboard = [["/dice", "/timer"]]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(
            "Возвращаемся к предыдущему меню", reply_markup=markup
        )
    else:
        if text == "30 секунд":
            due = 30
        elif text == "1 минута":
            due = 60
        elif text == "5 минут":
            due = 300
        elif text == "вернуться назад":
            reply_keyboard = [["/dice", "/timer"]]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            update.message.reply_text(
                "Возвращаемся к предыдущему меню",
                reply_markup=markup,
                entities="/start",
            )
        chat_id = update.message.chat_id
        try:

            job_removed = remove_job_if_exists(str(chat_id), context)
            context.job_queue.run_once(task, due, context=chat_id, name=str(chat_id))
            text = f"Засек {text}"
            if job_removed:
                text += " Старая задача удалена."
            # Присылаем сообщение о том, что всё получилось.
            reply_keyboard = [["/close"]]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            update.message.reply_text(text, reply_markup=markup)

        except (IndexError, ValueError):
            update.message.reply_text("Использование: /set <секунд>")


def task(context):
    """Выводит сообщение"""
    job = context.job
    context.bot.send_message(job.context, text="Время истекло")


def timer(update, context):
    reply_keyboard = [["30 секунд", "1 минута"], ["5 минут", "вернуться назад"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Засекай таймер", reply_markup=markup)


def close(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Таймер сброшен"
    reply_keyboard = [["/dice", "/timer"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text(text, reply_markup=markup)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("dice", dice))
    dp.add_handler(CommandHandler("timer", timer))
    dp.add_handler(CommandHandler("close", close))

    dp.add_handler(MessageHandler(Filters.text, set_timer))

    updater.start_polling()
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == "__main__":
    main()
