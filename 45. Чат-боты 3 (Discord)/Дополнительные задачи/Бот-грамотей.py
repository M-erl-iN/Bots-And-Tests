import discord
import pymorphy2
from auth import TOKEN
from discord.ext import commands

TOKEN = TOKEN


class Literal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.morph = pymorphy2.MorphAnalyzer()

    @commands.command(name="numerals")
    async def numerals(self, ctx, word, num):
        correct_answer = self.morph.parse(word)[0]
        result = str(num) + " " + correct_answer.make_agree_with_number(int(num)).word
        await ctx.send(result)
        await ctx.send(result)

    @commands.command(name="alive")
    async def alive(self, ctx, word):
        parse = self.morph.parse(word)[0]
        if parse.tag.POS == "NOUN":
            gender = str(parse.tag.gender)
            num = str(parse.tag.number)
            if parse.tag.animacy == "anim":
                if num == "plur":
                    live = self.morph.parse("живой")[0].inflect({"nomn", num}).word
                else:
                    live = (
                        self.morph.parse("живой")[0].inflect({"nomn", gender, num}).word
                    )
                result = f"{word} {live}"
            else:
                if num == "plur":
                    not_live = self.morph.parse("не живой")[0].inflect({num}).word
                else:
                    not_live = self.morph.parse("не живой")[0].inflect({gender}).word
                result = f"{word} {not_live}"
            await ctx.send(result)
        else:
            await ctx.send("Нужно ввести существительное")

    @commands.command(name="noun")  # #!noun питон ablt plur
    async def noun(self, ctx, word, case, num):
        parse = self.morph.parse(word)[0]
        correct_word = parse.inflect({case}).word
        await ctx.send(correct_word)

    @commands.command(name="inf")
    async def inf(self, ctx, word):
        parse = self.morph.parse(word)[0]
        correct_word = parse.normal_form
        await ctx.send(correct_word)

    @commands.command(name="morph")
    async def morph(self, ctx, word):
        parse = self.morph.parse(word)[0]
        await ctx.send(parse.tag)


bot = commands.Bot(command_prefix="#!")
bot.add_cog(Literal(bot))
bot.run(TOKEN)
