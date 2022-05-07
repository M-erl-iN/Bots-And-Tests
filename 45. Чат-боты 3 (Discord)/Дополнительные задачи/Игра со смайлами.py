import random

import discord
from auth import TOKEN
from discord.ext import commands

TOKEN = TOKEN


class Smiles(discord.Client):
    def __init__(self):
        super().__init__()
        self.smiles = [
            ("😀", 1),
            ("😍", 15),
            ("🤑", 28),
            ("😷", 50),
            ("🤠", 62),
            ("😈", 96),
            ("💀", 98),
            ("💩", 100),
            ("🤡", 101),
            ("👽", 105),
            ("🤖", 107),
            ("❤", 134),
            ("🐴", 529),
            ("🦄", 531),
            ("🦠", 626),
            ("🌈", 981),
        ]
        self.restart_game()

    def restart_game(self):
        self.current_game_smile_list = self.smiles.copy()
        self.player = 0
        self.bot = 0

    async def on_message(self, message):
        if message.author != self.user:
            if message.content == "/stop":
                await message.channel.send("Game stop")
                self.restart_game()
                return

            random.shuffle(self.current_game_smile_list)

            if int(message.content) >= len(self.current_game_smile_list):
                num = int(message.content) % len(self.current_game_smile_list)
            else:
                num = int(message.content)

            user_smile = self.current_game_smile_list[num]
            bot_smile = random.choice(self.current_game_smile_list)

            while bot_smile == user_smile:
                bot_smile = random.choice(self.current_game_smile_list)
            if user_smile[1] > bot_smile[1]:
                self.player += 1
            elif user_smile[1] < bot_smile[1]:
                self.bot += 1

            self.current_game_smile_list.remove(user_smile)
            self.current_game_smile_list.remove(bot_smile)

            if len(self.current_game_smile_list) == 0:
                if self.player > self.bot:
                    win = "You win"
                elif self.player < self.bot:
                    win = "Bot win"
                else:
                    win = "draw"
                message_send = f"""Emoticons are over
Score: You {self.player} - Bot {self.bot}
{win}!"""
                await message.channel.send(message_send)
                self.restart_game()
            else:
                message_send = f"""Your emoji {user_smile[0]}
Bot emoji {bot_smile[0]}
Score: You {self.player} - Bot {self.bot}"""
                await message.channel.send(message_send)


client = Smiles()
client.run(TOKEN)
