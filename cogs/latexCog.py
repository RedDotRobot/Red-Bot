import discord
from discord.ext import commands
import urllib.parse
import urllib.request
import io
from PIL import Image

class latexCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def generateFile(self, dpi, tex):
		url = "https://latex.codecogs.com/gif.latex?{0}"
		query = f"\\dpi{{{dpi}}} \\bg_white {tex}"
		imgBytes = io.BytesIO()
		url = url.format(urllib.parse.quote(query))
		img = Image.open(io.BytesIO(urllib.request.urlopen(url).read()))
		finalImg = Image.new("RGBA", (img.size[0]+20, img.size[1]+20), (255, 255, 255, 255))
		finalImg.paste(img, (10, 10))
		pixels = finalImg.getdata()
		for x in range(finalImg.width):
			for y in range(finalImg.height):
				pixel = finalImg.getpixel((x, y))
				if pixel[:3] == (255, 255, 255):
					finalImg.putpixel((x, y), (0, 0, 0, 0))
				elif pixel[:3] == (0, 0, 0):
					finalImg.putpixel((x, y), (255, 255, 255))
		finalImg.save(fp="variableImage/latexRender.png", format="PNG")
		imgBytes.seek(0)
		return imgBytes

	@commands.command()
	async def tex(self, ctx, *args):
		tex = "".join(args)
		await self.generateFile(200, tex)
		with open("variableImage/latexRender.png", "r") as f:
			await ctx.send(file=discord.File(f))

async def setup(bot):
	await bot.add_cog(latexCog(bot))