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
    response = vk.friends.get(fields=["nickname", "bdate"])
    friends = []
    if response["items"]:
        for i in response["items"]:
            if "bdate" in i.keys():
                friends.append((i["last_name"], i["first_name"], i["bdate"]))
            else:
                friends.append(
                    (i["last_name"], i["first_name"], "Дата рождения отсутствует")
                )
    friends = sorted(friends, key=lambda x: x[0])
    for friend in friends:
        print(friend[0] + " " + friend[1], friend[2])


if __name__ == "__main__":
    main()
