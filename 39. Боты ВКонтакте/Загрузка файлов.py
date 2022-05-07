import requests
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
    album_id = 278222474
    group_id = 203303842
    files = {
        "file1": open("static/img/Picture1.jpg", "rb"),
        "file2": open("static/img/Picture2.jpg", "rb"),
        "file3": open("static/img/Picture3.jpg", "rb"),
    }

    upload_url = vk.photos.getUploadServer(album_id=album_id, group_id=group_id)[
        "upload_url"
    ]
    response = requests.post(upload_url, files=files).json()

    server = response["server"]
    photos_list = response["photos_list"]
    aid = response["aid"]
    response_hash = response["hash"]

    vk.photos.save(
        album_id=album_id,
        group_id=group_id,
        server=server,
        photos_list=photos_list,
        aid=aid,
        hash=response_hash,
    )


if __name__ == "__main__":
    main()
