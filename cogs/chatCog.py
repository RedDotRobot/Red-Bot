import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("openAPIKey")

class chatCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def chat(ctx, *args):
		prompt = " ".join(args)
		response = openai.Completion.create(
			engine="text-davinci-002",
			prompt=prompt,
			max_tokens=1024,
			n=1,
			stop=None
)
		text = response['choices'][0]['text']
		embed = discord.Embed(title="OpenAI Chat Bot")
		embed.add_field(name=f"{prompt}", value=text)
		await ctx.send(embed=embed)

async def setup(bot):
	await bot.add_cog(chatCog(bot))