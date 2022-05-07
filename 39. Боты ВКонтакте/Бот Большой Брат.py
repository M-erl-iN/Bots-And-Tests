import random

import vk_api
from auth import TOKEN
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

            response = vk.users.get(
                user_ids=event.obj.message["from_id"], fields=["city"]
            )[0]
            name = response["first_name"]
            message = f"Привет, {name}!"

            if "city" in response.keys():
                city = response["city"]["title"]
                message = f"Привет, {name}!" + f" Как поживает {city}?"

            vk.messages.send(
                user_id=event.obj.message["from_id"],
                message=message,
                random_id=random.randint(0, 2**64),
            )


if __name__ == "__main__":
    main()
