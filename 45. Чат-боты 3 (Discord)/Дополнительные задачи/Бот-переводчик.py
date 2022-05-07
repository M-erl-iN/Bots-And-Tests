import random

import discord
from auth import TOKEN
from deep_translator import GoogleTranslator
from discord.ext import commands

TOKEN = TOKEN


# pip install deep-translator


class TranslateBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.source = "en"
        self.target = "ru"

    @commands.command(name="help_bot")
    async def help(self, ctx):
        help_text = """Я бот-переводчик, я умею:\n
!!set_lang <lang>-<lang> - сменить язык,\n
!!text <text> - перевести текст\n
!!help_bot - помощь"""
        await ctx.send(help_text)

    @commands.command(name="set_lang")  # !!set_lang ru-pl
    async def set_language(self, ctx, lang):
        self.source, self.target = lang.split("-")
        print(self.source, self.target)
        await ctx.send("Type '!!text and text for translate'")

    @commands.command(name="text")
    async def translate_text(self, ctx, *text):
        text = " ".join(text)
        translated = GoogleTranslator(source=self.source, target=self.target)
        await ctx.send(translated.translate(text))


bot = commands.Bot(command_prefix="!!")
bot.add_cog(TranslateBot(bot))
bot.run(TOKEN)
