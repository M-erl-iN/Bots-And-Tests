import random

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

TOKEN = TOKEN
group_id = 203303842


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

            url = f"photo-203303842_{get_img_id()}"
            vk.messages.send(
                user_id=event.obj.message["from_id"],
                message=message,
                random_id=random.randint(0, 2**64),
                attachment=url,
            )


def get_img_id():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    album_id = 278222474
    group_id = -203303842

    response = vk.photos.get(owner_id=group_id, album_id=album_id, photo_sizes=1)
    items = response["items"]
    item = random.choice(items)
    return item["id"]


if __name__ == "__main__":
    main()
