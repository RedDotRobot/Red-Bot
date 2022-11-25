import discord
from discord.ext import commands
import logging
import datetime
import os
import requests
import json
import asyncio

#Weather ID lists
clearWeather = ["800", "801"]
cloudyWeather = ["802", "803", "804"]
drizzleWeather = ["300", "301", "310", "311", "500", "520"]
rainWeather = ["302", "312", "313", "314", "321", "501", "502", "503", "504", "511", "521", "522", "531"]
thunderstormWeather = ["200", "201", "202", "210", "211", "212", "221", "230", "231", "232"]
snowWeather = ["600", "601", "602", "611", "612", "613", "615", "616", "620", "621", "622"]
otherWeather = ["701", "711", "721", "731", "741", "751", "761", "762", "771", "781"]

class informationCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		global log
		log = logging.getLogger("red-bot.py")

	def weather(self):
			url = os.getenv("weatherURL")
			response = requests.get(url)
			data = json.loads(response.text)
			weather = data["weather"]
			weatherID = str(weather[0]["id"])
			weatherDescription = weather[0]["description"]
			weatherDescription = weatherDescription.capitalize()
			temp = data["main"]["temp"]
			feelTemp = data["main"]["feels_like"]
			minTemp = data["main"]["temp_min"]
			maxTemp = data["main"]["temp_max"]
			humidity = data["main"]["humidity"]
			if weatherID in clearWeather: #Clear
				file = discord.File("Weather_Images/clearWeatherIMG.gif")
				embed.set_image(url="attachment://clearWeatherIMG.gif")
			elif weatherID in cloudyWeather: #Cloudy
				file = discord.File("Weather_Images/cloudyWeatherIMG.gif")
				embed.set_image(url="attachment://cloudyWeatherIMG.gif")
			elif weatherID in drizzleWeather: #Drizzle
				file = discord.File("Weather_Images/drizzleWeatherIMG.gif")
				embed.set_image(url="attachment://drizzleWeatherIMG.gif")
			elif weatherID in rainWeather: #Rain
				file = discord.File("Weather_Images/rainWeatherIMG.gif")
				embed.set_image(url="attachment://rainWeatherIMG.gif")	
			elif weatherID in thunderstormWeather: #Thunderstorm
				file = discord.File("Weather_Images/thunderstormWeatherIMG.gif")
				embed.set_image(url="attachment://thunderstormWeatherIMG.gif")
			elif weatherID in snowWeather: #Snow
				file = discord.File("Weather_Images/snowWeatherIMG.gif")
				embed.set_image(url="attachment://snowWeatherIMG.gif")

	@commands.command(aliases=["information"])
	async def info(self, ctx):
		#Time and date
		currentTime = datetime.now()
		time = currentTime.strftime("%H:%M:%S")
		date = currentTime.strftime("%d/%m/%Y")
		await ctx.channel.purge(limit=999) #Clear channel
		generalInfo = discord.Embed(title=f"Dashboard | {date}", description=f"**{time}**")
		generalInfo.add_field(name=f"ping", value=f"{self.bot.latency*1000:0.2f}ms")
		msg = await ctx.send(embed=generalInfo)
		while True:
			generalInfo = discord.Embed(description=f"{time}")
			asyncio.sleep(1)
			msg.edit(embed=generalInfo)

async def setup(bot):
	await bot.add_cog(informationCog(bot))
