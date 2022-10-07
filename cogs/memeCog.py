from discord.ext import commands
import random

class memeCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def hibye(self, ctx):
		await ctx.send("https://c.tenor.com/xmCVYPzu_j8AAAAC/simpsons-bart-simpson.gif")

	@commands.command()
	async def thisisfine(self, ctx):
		await ctx.send("https://c.tenor.com/MYZgsN2TDJAAAAAC/this-is.gif")

	@commands.command(aliases=["fd", "dad"])
	async def finddad(self, ctx):
		with open("finddad_responses.txt") as f:
			line = f.readlines()
		output = str(random.choice(line))
		await ctx.send(output)

async def setup(bot):
	await bot.add_cog(memeCog(bot))