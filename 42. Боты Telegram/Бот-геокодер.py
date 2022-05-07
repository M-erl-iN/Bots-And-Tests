import json

import requests
from auth import TOKEN
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)


def start(update, context):
    text = (
        "Привет! Я бот-геокодер, я могу показать карту с "
        "местностью, просто введи /map <местность.>"
    )
    update.message.reply_text(text)


def geocoder(update, context):
    geocoder_uri = geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(
        geocoder_uri,
        params={
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "format": "json",
            "geocode": context.args[0],
        },
    )

    result = get_parameters(response)
    if "Error" in type(result).__name__:
        if type(result).__name__ == "IndexError":
            update.message.reply_text(f"Ничего не найдено")
        else:
            update.message.reply_text(f"Неизвестная ошибка: {type(result)}")
    else:
        static_api_request, annotation = get_parameters(response)

        context.bot.send_photo(
            update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
            # Ссылка на static API, по сути, ссылка на картинку.
            # Телеграму можно передать прямо её, не скачивая предварительно карту.
            static_api_request,
            caption=f"{annotation}",
        )


def get_parameters(response):
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    try:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
            "GeoObject"
        ]
        annotation = toponym["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"][
            "Country"
        ]["AddressLine"]
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]
        # Долгота и широта:
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    except Exception as error:
        return error

    delta = "0.005"

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": "map",
        "pt": ",".join([toponym_longitude, toponym_lattitude, "pm2rdl"]),
        "caption": str(toponym_coodrinates),
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"

    return requests.get(map_api_server, params=map_params).url, annotation


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("map", geocoder, pass_args=True))

    updater.start_polling()
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == "__main__":
    main()
