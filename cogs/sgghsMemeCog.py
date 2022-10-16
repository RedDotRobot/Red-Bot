from discord.ext import commands
import logging, coloredlogs

class sgghsMemeCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		global log
		log = logging.getLogger("red-bot.py")

	@commands.command(aliases=["kiara", "dog"])
	async def kimchi(self, ctx):
		await ctx.send("🍽️🐶❤️")
		log.info(msg=f"{ctx.message.guild} > #{ctx.message.channel} | {ctx.message.author} | !kimchi")

	@commands.command()
	async def monkey(self, ctx):
		await ctx.send("same relatable penis among us !! h ok funny moneky")
		await ctx.send("https://media.tenor.com/0_6MYrn00tMAAAAd/monkey-kinkytwt.gif")
		log.info(msg=f"{ctx.message.guild} > #{ctx.message.channel} | {ctx.message.author} | !monkey")

	@commands.command(aliases=["abtin"])
	async def adiba(self, ctx):
		await ctx.send("adiba ❤️ abtin")
		log.info(msg=f"{ctx.message.guild} > #{ctx.message.channel} | {ctx.message.author} | !adiba")

	@commands.command()
	async def matilda(self, ctx):
		await ctx.send("chloe smells like ms di leo")
		await ctx.send("https://media.tenor.com/AukNDGqQS2UAAAAC/bitmoji-emoji.gif")
		log.info(msg=f"{ctx.message.guild} > #{ctx.message.channel} | {ctx.message.author} | !matilda")

	@commands.command()
	async def sylvia(self, ctx):
		await ctx.send("sylvia is mean :(")
		log.info(msg=f"{ctx.message.guild} > #{ctx.message.channel} | {ctx.message.author} | !sylvia")

	@commands.command()
	async def lloyd(self, ctx):
		await ctx.send("send lloyd dick pics")
		log.info(msg=f"{ctx.message.guild} > #{ctx.message.channel} | {ctx.message.author} | !lloyd")

async def setup(bot):
	await bot.add_cog(sgghsMemeCog(bot))