import datetime
import random

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

TOKEN = TOKEN
group_id = "203303842"


#  LongPoll API == API 5.103


def main():
    vk_session = vk_api.VkApi(token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, group_id)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            if any(
                [
                    True
                    for i in ["время", "число", "дата", "день"]
                    if i in event.obj.message["text"]
                ]
            ):

                date = datetime.datetime.now().strftime("%d.%m.%Y")
                time = datetime.datetime.now().strftime("%H:%M:%S")

                week_days = [
                    "Понедельник",
                    "Вторник",
                    "Среда",
                    "Четверг",
                    "Пятница",
                    "Суббота",
                    "Воскресенье",
                ]
                weekday = week_days[datetime.datetime.now().weekday()]

                message = f"Дата: {date} \n Время: {time} \n День недели: {weekday}"
                vk.messages.send(
                    user_id=event.obj.message["from_id"],
                    message=message,
                    random_id=random.randint(0, 2**64),
                )
            else:
                message = f'Напиши слово "дата" и увидишь что я могу!'
                vk.messages.send(
                    user_id=event.obj.message["from_id"],
                    message=message,
                    random_id=random.randint(0, 2**64),
                )


if __name__ == "__main__":
    main()
