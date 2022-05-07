import json

import requests
from auth import TOKEN
from discord.ext import commands

TOKEN = TOKEN


def get_weather(lat, lon):
    headers = {"X-Yandex-API-Key": "942004fe-1485-48c7-93b2-95106dad588e"}
    params = {"lat": lat, "lon": lon, "lang": "ru_RU", "limit": 7, "hours": "false"}
    response = requests.get(
        "https://api.weather.yandex.ru/v2/forecast", headers=headers, params=params
    )

    return response.json()


class WeatherBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.geocode = "Moscow"

    @commands.command(name="help_bot")
    async def help(self, ctx):
        help_text = """Я бот-метеоролог, я умею:\n
#!place <место> - задаёт место прогноза,\n
#!forecast <дни> - сообщает прогноз погоды на указанное кол-во дней\n
!!help_bot - помощь"""
        await ctx.send(help_text)

    @commands.command(name="place")
    async def set_place(self, ctx, *args):
        self.geocode = " ".join(args)
        await ctx.send(f"Place changed to {self.geocode}")

    def get_coordinates(self):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.geocode,
            "format": "json",
        }
        response = requests.get(geocoder_api_server, params=geocoder_params).json()[
            "response"
        ]
        toponym = response["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        lon, lat = toponym["Point"]["pos"].split()
        return lon, lat

    @commands.command(name="forecast")
    async def weather_days(self, ctx, days):
        lon, lat = self.get_coordinates()
        weather_response = get_weather(lat, lon)
        response_text = """"""
        weather_days = weather_response["forecasts"][: int(days)]
        for day in weather_days:
            date = day["date"]
            temp = day["parts"]["day"]["temp_avg"]
            pressure = day["parts"]["day"]["pressure_mm"]
            humidity = day["parts"]["day"]["humidity"]
            condition = day["parts"]["day"]["condition"]
            wind_dir = day["parts"]["day"]["wind_dir"]
            wind_speed = day["parts"]["day"]["wind_speed"]
            response_text += f"""Weather forecast in {self.geocode} for {date}
Temperature: {temp},
Pressure: {pressure}mm,
Humidity: {humidity}%,
{condition},
Wind {wind_dir}, {wind_speed} m/s.\n\n\n"""
        await ctx.send(response_text)

    @commands.command(name="current")
    async def current(self, ctx):
        lon, lat = self.get_coordinates()
        weather_response = get_weather(lat, lon)
        weather_now_info = weather_response["fact"]
        temp = weather_now_info["temp"]
        pressure = weather_now_info["pressure_mm"]
        humidity = weather_now_info["humidity"]
        condition = weather_now_info["condition"]
        wind_dir = weather_now_info["wind_dir"]
        wind_speed = weather_now_info["wind_speed"]
        response_text = f"""Current Weather in {self.geocode}
Temperature: {temp},
Pressure: {pressure}mm,
Humidity: {humidity}%,
{condition},
Wind {wind_dir}, {wind_speed} m/s."""
        await ctx.send(response_text)


bot = commands.Bot(command_prefix="#!")
bot.add_cog(WeatherBot(bot))
bot.run(TOKEN)
