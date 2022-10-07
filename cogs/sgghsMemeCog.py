from discord.ext import commands

class sgghsMemeCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=["kiara"])
	async def kimchi(self, ctx):
		await ctx.send("🍽️🐶❤️")

	@commands.command()
	async def monkey(self, ctx):
		await ctx.send("same relatable penis among us !! h ok funny moneky")
		await ctx.send("https://media.tenor.com/0_6MYrn00tMAAAAd/monkey-kinkytwt.gif")

	@commands.command(aliases=["abtin"])
	async def adiba(self, ctx):
		await ctx.send("adiba ❤️ abtin")

	@commands.command()
	async def matilda(self, ctx):
		await ctx.send("chloe smells like ms di leo")
		await ctx.send("https://media.tenor.com/AukNDGqQS2UAAAAC/bitmoji-emoji.gif")

	@commands.command()
	async def sylvia(self, ctx):
		await ctx.send("sylvia is mean :(")

	@commands.command()
	async def lloyd(self, ctx):
		await ctx.send("send lloyd dick pics")

async def setup(bot):
	await bot.add_cog(sgghsMemeCog(bot))