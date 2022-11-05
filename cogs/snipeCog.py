from calendar import c
from discord.ext import commands
import asyncio
import logging, coloredlogs

class snipeCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		global log
		log = logging.getLogger("red-bot.py")

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		global snipe_message_author
		global snipe_message_content
		snipe_message_author = {}
		snipe_message_content = {}
		snipe_message_author[message.channel.id] = message.author
		snipe_message_content[message.channel.id] = message.content
		await asyncio.sleep(3600)
		del snipe_message_author[message.channel.id]
		del snipe_message_content[message.channel.id]
		with open("cogs/snipe.log", "a") as f:
			f.write(f"User {snipe_message_author[message.channel.id]} deleted {snipe_message_content[message.channel.id]}\n")

	@commands.command()
	async def snipe(self, ctx):
		channel = ctx.channel
		try:
			await ctx.send(f"User {snipe_message_author[channel.id]} deleted \"{snipe_message_content[channel.id]}\"")
			log.info(msg=f"{ctx.message.guild} > #{ctx.message.channel} | {ctx.message.author} | !snipe | Returned deleted message")
		except:
			await ctx.send(f"No recently deleted messages in #{channel.name}")
			log.info(msg=f"{ctx.message.guild} > #{ctx.message.channel} | {ctx.message.author} | !snipe | Error: No deleted messages")

async def setup(bot):
	await bot.add_cog(snipeCog(bot))
