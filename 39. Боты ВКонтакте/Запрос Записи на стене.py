import datetime

import vk_api


def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    # Используем метод wall.get
    response = vk.wall.get(count=5, offset=1)
    if response["items"]:
        for i in response["items"]:
            text = i["text"]
            date = datetime.datetime.fromtimestamp(i["date"]).strftime("%Y-%m-%d")
            time = datetime.datetime.fromtimestamp(i["date"]).strftime("%H:%M:%S")
            print(f"Text: {text}")
            print(f"date: {date}, time: {time}")
            print("-------------------------")


if __name__ == "__main__":
    main()
