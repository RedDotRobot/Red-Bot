from discord.ext import commands
import asyncio
import logging, coloredlogs

log = logging.getLogger("red-bot.py")
coloredlogs.install(level="INFO", fmt="%(asctime)s [%(levelname)s] %(message)s")
coloredlogs.DEFAULT_FIELD_STYLES = "spam=22;debug=220;info=34;notice=220;warning=202;success=118,bold;error=124;critical=background=red"

class snipeCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		global snipe_message_author
		global snipe_message_content

	@commands.event()
	async def on_message_delete(self, message):
		snipe_message_author = {}
		snipe_message_content = {}
		snipe_message_author[message.channel.id] = message.author
		snipe_message_content[message.channel.id] = message.content
		await asyncio.sleep(3600)
		del snipe_message_author[message.channel.id]
		del snipe_message_content[message.channel.id]
	
	@commands.command()
	async def snipe(self, ctx):
		channel = ctx.channel
		try:
			ctx.send(f"User {snipe_message_author[channel.id]} deleted \"{snipe_message_content[channel.id]}\"")
			log.info(msg=f"{ctx.message.guild} > #{ctx.message.channel} | {ctx.message.author} | !snipe | Returned deleted message")
			
		except KeyError:
			await ctx.send(f"No recently deleted messages in #{channel.name}")
			log.info(msg=f"{ctx.message.guild} > #{ctx.message.channel} | {ctx.message.author} | !snipe | Error: No deleted messages")

async def setup(bot):
	await bot.add_cog(snipeCog(bot))
