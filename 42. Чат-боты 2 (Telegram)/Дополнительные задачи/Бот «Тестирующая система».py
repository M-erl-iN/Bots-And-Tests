import json
import random

from auth import TOKEN
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

questions = json.load(open("file.json", encoding="utf-8"))["test"]


def start(update, context):
    num = random.randint(0, len(questions) - 1)
    text = (
        f"Пройдите опрос и проверьте свои знания!\n\n"
        f"Вопрос №1 : {questions[num]['question']}"
    )
    context.user_data["history_questions"] = [questions[num]]
    update.message.reply_text(text)
    return 1


def get_question(update, context):
    text = update.message.text

    if len(context.user_data.keys()) == 1:
        context.user_data["count_question"] = 0
        context.user_data["count_corr_answers"] = 0

    for quest in questions:
        if quest == context.user_data["history_questions"][-1]:
            question = quest
    if text == question["response"]:
        context.user_data["count_corr_answers"] += 1

    if context.user_data["count_question"] == len(questions) - 1:
        update.message.reply_text(
            f"Вы прошли тест! Кол-во правильных ответов: "
            f"{context.user_data['count_corr_answers']}. "
            f"Пройдите текст снова!"
        )
        context.user_data["count_question"] = 0
        context.user_data["count_corr_answers"] = 0
        context.user_data["history_questions"] = []
        return ConversationHandler.END

    question = random.choice(questions)
    while question in context.user_data["history_questions"]:
        question = random.choice(questions)

    context.user_data["history_questions"].append(question)
    context.user_data["count_question"] += 1

    text = f"Вопрос №{context.user_data['count_question'] + 1} : {question['question']}"
    update.message.reply_text(text)
    return 1


def stop(update, context):
    update.message.reply_text("Тест закончен")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            1: [
                CommandHandler("stop", stop),
                MessageHandler(Filters.text, get_question, pass_user_data=True),
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
