from cmath import phase
from email import header
from tkinter import E
import discord
from discord.ext import commands
import logging, coloredlogs
from googletrans import Translator, constants

class translateCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		global log
		global tr
		log = logging.getLogger("red-bot.py")
		tr = Translator()

	@commands.command(aliases=["tr", "translation"])
	async def translate(self, ctx, *args):
		phrase = " ".join(args)
		translation = tr.translate(phrase)
		embed = discord.Embed(title="Translation							ㅤ")
		embed.add_field(name=f"{translation.src.upper()}", value=f"{translation.origin}\n", inline=True)
		embed.add_field(name=f"{translation.dest.upper()}", value=f"{translation.text.capitalize()}", inline=False)
		await ctx.send(embed=embed)

async def setup(bot):
	await bot.add_cog(translateCog(bot))