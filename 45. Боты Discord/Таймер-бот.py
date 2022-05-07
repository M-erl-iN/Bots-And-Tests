import asyncio

import discord
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
                f"И готов ставить таймер"
            )

    async def on_message(self, message):
        if message.author != self.user:
            text = message.content.lower()
            if "set_timer" in text:
                try:
                    words = text.split()
                    hours = int(words[2])
                    minutes = int(words[4])
                except (IndexError, ValueError):
                    await message.channel.send("Неправильный ввод")
                    return
                await message.channel.send(
                    f"The timer should start in {hours} and {minutes} minutes."
                )
                await asyncio.sleep(hours * 3600 + minutes * 60)
                await message.channel.send(f"Time X has come!")


client = CatOrDog()
client.run(TOKEN)
