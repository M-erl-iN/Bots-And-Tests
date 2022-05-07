import random

import vk_api
import wikipedia
from auth import TOKEN
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

TOKEN = TOKEN
group_id = "203303842"


#  LongPoll API == API 5.103


def main():
    vk_session = vk_api.VkApi(token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, group_id)

    first_message = False

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            text = event.obj.message["text"]
            if not first_message:
                message = "Привет! Я вики-бот, я знаю о многом. Хочешь что-то узнать?"
                first_message = True
            else:
                wikipedia.set_lang("ru")
                try:
                    message = wikipedia.summary(text, sentences=5)
                except wikipedia.exceptions.PageError:
                    message = "К сожалению, я ничего не нашел по этому запросу"
                message += "\n \n \n Может ты хочешь узнать что-то еще?"
            vk.messages.send(
                user_id=event.obj.message["from_id"],
                message=message,
                random_id=random.randint(0, 2**64),
            )


if __name__ == "__main__":
    main()
