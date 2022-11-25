from discord.ext import commands
import random
import logging

class memeCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		global log
		log = logging.getLogger("red-bot.py")

	@commands.command()
	async def hibye(self, ctx):
		await ctx.send("https://c.tenor.com/xmCVYPzu_j8AAAAC/simpsons-bart-simpson.gif")
		log.info(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !hibye")

	@commands.command()
	async def thisisfine(self, ctx):
		await ctx.send("https://c.tenor.com/MYZgsN2TDJAAAAAC/this-is.gif")
		log.info(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !thisisfine")

	@commands.command(aliases=["fd", "dad"])
	async def finddad(self, ctx):
		with open("finddad_responses.txt") as f:
			line = f.readlines()
		output = str(random.choice(line))
		await ctx.send(output)
		log.info(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !finddad")

	@commands.command(aliases=["roast"])
	async def insult(self, ctx):
		with open("insults.txt") as f:
			line = f.readlines()
		output = str(random.choice(line))
		await ctx.send(output)
		log.info(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !insult")

async def setup(bot):
	await bot.add_cog(memeCog(bot))