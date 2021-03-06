from auth import TOKEN
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater


def help(update, context):
    update.message.reply_text("Я пока не умею помогать...")


def start(update, context):
    reply_keyboard = [["/set_timer", "/unset"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Я бот-даты и времени.", reply_markup=markup)


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text("Извините, не умеем возвращаться в прошлое")
            return

        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(task, due, context=chat_id, name=str(chat_id))
        text = f"Вернусь через {due} секунд!"
        if job_removed:
            text += " Старая задача удалена."
        # Присылаем сообщение о том, что всё получилось.
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text("Использование: /set_timer <секунд>")


def task(context):
    """Выводит сообщение"""
    job = context.job
    context.bot.send_message(job.context, text="Вернулся!")


def unset_timer(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Хорошо, вернулся сейчас!" if job_removed else "Нет активного таймера."
    update.message.reply_text(text)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(
        CommandHandler(
            "set_timer",
            set_timer,
            pass_args=True,
            pass_job_queue=True,
            pass_chat_data=True,
        )
    )
    dp.add_handler(CommandHandler("unset", unset_timer, pass_chat_data=True))

    updater.start_polling()
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == "__main__":
    main()
