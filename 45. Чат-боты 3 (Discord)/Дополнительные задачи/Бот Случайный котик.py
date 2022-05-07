import discord
import requests
from auth import TOKEN
from discord.ext import commands

TOKEN = TOKEN


class CatOrDog(discord.Client):
    async def on_ready(self):
        print(f"{self.user} подключился к Дискорду!")
        for guild in self.guilds:
            print(
                f"{self.user} подключился к чату:\n"
                f"{guild.name}(id: {guild.id})\n"
                f"И готов показывать случайного котика (или пёсика!)."
            )

    async def on_message(self, message):
        if message.author != self.user:
            if "кот" in message.content.lower() or "кош" in message.content.lower():
                url = requests.get("https://api.thecatapi.com/v1/images/search").json()[
                    0
                ]["url"]
                await message.channel.send(url)
            elif (
                "соба" in message.content.lower()
                or "пес" in message.content.lower()
                or "пёс" in message.content.lower()
            ):
                url = requests.get("https://dog.ceo/api/breeds/image/random").json()[
                    "message"
                ]
                await message.channel.send(url)


client = CatOrDog()
client.run(TOKEN)
