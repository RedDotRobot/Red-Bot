from discord.ext import commands
import asyncio
import logging, coloredlogs

class snipeCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		global log
		log = logging.getLogger("red-bot.py")

	@commands.Cog.listener()
	async def on_member_join(self, ctx, member):
		if ctx.guild.id == 944908507768045619:
			with open("whitelist.txt") as f:
				if member.id in f.read():
					pass
				else:
					await member.ban(reason="User ID not whitelisted.")
					log.info(f"{ctx.message.guild} » #{ctx.message.channel} | {member.name} | whitelist » User {member.name} was banned.")

async def setup(bot):
	await bot.add_cog(snipeCog(bot))
