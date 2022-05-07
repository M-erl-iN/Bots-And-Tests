import vk_api
from auth import LOGIN, PASSWORD


def main():
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
    for item in items:
        photos = item["sizes"]
        for photo in photos:
            height = photo["height"]
            width = photo["width"]
            url = photo["url"]
            print(f"Ширина: {width}, Высота: {height}, Ссылка на фото: {url}")


if __name__ == "__main__":
    main()
