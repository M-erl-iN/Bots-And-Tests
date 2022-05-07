import datetime
import random

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

TOKEN = TOKEN
group_id = "203303842"


#  LongPoll API == API 5.103


def main():
    vk_session = vk_api.VkApi(token=TOKEN)

    first_message = False

    longpoll = VkBotLongPoll(vk_session, group_id)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            if not first_message:
                message = (
                    f"Привет! Я могу сказать в какой день недели была какая-нибудь дата, "
                    f"введи её в формате YYYY-MM-DD"
                )
                first_message = True
            else:
                week_days = [
                    "Понедельник",
                    "Вторник",
                    "Среда",
                    "Четверг",
                    "Пятница",
                    "Суббота",
                    "Воскресенье",
                ]
                try:
                    date = datetime.datetime.strptime(
                        event.obj.message["text"], "%Y-%m-%d"
                    )
                    weekday = week_days[date.weekday()]
                    message = weekday
                except ValueError:
                    message = (
                        "Вы ввели неправильную дату, введите снова в формате YYYY-MM-DD"
                    )

            vk.messages.send(
                user_id=event.obj.message["from_id"],
                message=message,
                random_id=random.randint(0, 2**64),
            )


if __name__ == "__main__":
    main()
