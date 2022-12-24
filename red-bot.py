#Import Modules
import asyncio
import os
import sys
import discord										#Discord stuff
from discord.ext import commands
from dotenv import load_dotenv						#.env
from datetime import datetime						#Datetime
import requests										#JSON Requests
import json
import yfinance as yf								#ASX lesh go
import plotly.graph_objs as go
import os.path
import logging, coloredlogs
import winsound
import random

#Introduce Bot
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, activity=discord.Activity(type=discord.ActivityType.listening, name="the cries of young children"), help_command=None)
load_dotenv()
botToken = os.getenv("botToken")
yf.pdr_override()
botStatus = "online"
botClock = "offline"

#Logger
log = logging.getLogger("red-bot.py")
coloredlogs.install(level="INFO", fmt="%(asctime)s [%(levelname)s] %(message)s")
coloredlogs.DEFAULT_FIELD_STYLES = "spam=22;debug=220;info=34;notice=220;warning=202;success=118,bold;error=124;critical=background=red"
fh = logging.FileHandler("bot.log")
fh.setLevel(logging.INFO)
log.addHandler(fh)

#Do all the weird time shit
def currentDatetime(format):
	if format == "time":
		currentTime = datetime.now()
		formatTime = currentTime.strftime("%H:%M:%S")
		return formatTime
	if format == "date":
		currentTime = datetime.now()
		formatDate = currentTime.strftime("%d/%m/%Y")
		return formatDate

#Define custom emojis
onlineStatus = "<:onlineStatus:994214218700169216>"
idleStatus = "<:idleStatus:994214221812338688>"
errorStatus = "<:errorStatus:994214217026650122>"
offlineStatus = "<:offlineStatus:994214206004019210>"
mrLatimer = "<:mrlatimer:1002519171365613578>"

#Weather ID lists
clearWeather = ["800", "801"]
cloudyWeather = ["802", "803", "804"]
drizzleWeather = ["300", "301", "310", "311", "500", "520"]
rainWeather = ["302", "312", "313", "314", "321", "501", "502", "503", "504", "511", "521", "522", "531"]
thunderstormWeather = ["200", "201", "202", "210", "211", "212", "221", "230", "231", "232"]
snowWeather = ["600", "601", "602", "611", "612", "613", "615", "616", "620", "621", "622"]
otherWeather = ["701", "711", "721", "731", "741", "751", "761", "762", "771", "781"]

@bot.event
async def on_ready():
	global botLogChannel
	await logInfo(f"Successfully logged in as {bot.user.name}")
	winsound.Beep(440, 500)
	botLogChannel = bot.get_channel(1038017545690693702)

@bot.command(aliases=["c","calculate"])
async def calc(ctx, arg):
	equation = str(arg)
	equation = equation.replace("x", "*").replace("÷", "/").replace(",", "").replace("^", "**").replace("k", "*1000").replace("m", "*1000000").replace("b", "*1000000000").replace(")(", ")*(")
	equation = equation.replace("0(", "0*(").replace("2(", "2*(").replace("3(", "3*(").replace("4(", "4*(").replace("5(", "5*(").replace("6(", "6*(").replace("7(", "7*(").replace("8(", "8*(").replace("9(", "9*(").replace(")0", ")*0").replace(")2", ")*2").replace(")3", ")*3").replace(")4", ")*4").replace(")5", ")*5").replace(")6(", ")*6").replace(")7", ")*7").replace(")8", ")*8").replace(")9", ")*9")
	result = eval(equation)
	result = f"{result:,.15f}".rstrip("0").rstrip(".")
	await ctx.send(result)
	await logInfo(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !calc")

@bot.command(aliases=["p","latency"])
async def ping(ctx):
	latency = f"{bot.latency*1000:0.2f}"
	embed=discord.Embed(title="Bot Latency", description=f"Current ping is {latency}ms")
	time = currentDatetime("time")
	date = currentDatetime("date")
	embed.set_footer(text=f"Today at {time} | {date}")
	await ctx.send(embed=embed)
	await logInfo(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !ping » {latency}")

@bot.command(aliases=["w"])
async def weather(ctx):
	#Grab Data
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
	embed=discord.Embed(title="**Weather Report**", url="https://www.msn.com/en-au/weather/weathertoday/Sydney-CBD,NSW,Australia/we-city?iso=AU&sethome=true&el=50s01jWY87RMHiXLHjA2pA%3D%3D&day=7&day=10", color=0x00dde0)
	embed.add_field(name="Current temperature ㅤ", value=f"{temp}°C", inline=True)
	embed.add_field(name="Weather			 ㅤ", value=f"{weatherDescription}", inline=True)
	embed.add_field(name = chr(173), value = chr(173)) #Embed linebreak
	embed.add_field(name="Feels Like		  ㅤ", value=f"{feelTemp}°C", inline=True)
	embed.add_field(name="Humidity			ㅤ", value=f"{humidity}%", inline=True)
	embed.add_field(name="Temperature range   ㅤ", value=f"{minTemp}°C - {maxTemp}°C", inline=True)
	embed.set_image(url="attachment://")
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
	time = currentDatetime("time")
	date = currentDatetime("date")
	embed.set_footer(text=f"Today at {time} | {date}")
	await ctx.send(file=file, embed=embed)
	await logInfo(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !weather")

@bot.command(aliases=["a","stock"])
async def asx(ctx, arg):
	data = yf.download(tickers=arg, period="3mo", interval="1d")
	fig = go.Figure()
	fig.add_trace(go.Candlestick(x=data.index, open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"], name = "market data"))
	arg = arg.upper()
	fig.update_layout(
		title=f"{arg} Trade Prices (3 Months)",
		yaxis_title="Stock Price (USD per Shares)")
	fig.write_image("variableImage/stockData.png")
	embed = discord.Embed(title=f"{arg} Stock Information")
	file = discord.File("variableImage/stockData.png")
	embed.set_image(url="attachment://stockData.png")
	time = currentDatetime("time")
	date = currentDatetime("date")
	embed.set_footer(text=f"Today at {time} | {date}")
	await ctx.send(file=file, embed=embed)
	await logInfo(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !asx | Stock value of {arg}")

@bot.command(aliases=["poll", "survey"])
async def suggest(ctx, title, option1, option2):
	embed=discord.Embed(title="Suggestion", description=title)
	embed.add_field(name=option1, value="🔴", inline=True)
	embed.add_field(name=option2, value="🔵", inline=True)
	time = currentDatetime("time")
	date = currentDatetime("date")
	embed.set_footer(text=f"Today at {time} | {date}")
	msg = await ctx.send(embed=embed)
	await msg.add_reaction("🔴")
	await msg.add_reaction("🔵")
	await logInfo(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !suggest")

@bot.command(aliases=["delete","clear"])
async def purge(ctx, limit:int):
	if ctx.author.id == 840418841942294548:
		limit = limit + 1
		await ctx.channel.purge(limit=limit)
		await logInfo(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !purge » Deleted {limit-1} messages")
	else:
		await ctx.send("Insufficient permissions")
		await logInfo(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !purge » Insufficient permissions")

@bot.command(aliases=["servers", "serverlist"])
async def server(ctx):
	serverlist = list()
	activeservers = bot.guilds
	for guild in activeservers:
		serverlist.append(guild.name)
	await ctx.send("\n".join(map(str, serverlist)))
	await logInfo(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !serverlist")

@bot.command(aliases=["t","status","botstatus"])
async def test(ctx):
	embed = discord.Embed(title="Bot Status", description=f"{onlineStatus} Bot is currently functional")
	time = currentDatetime("time")
	date = currentDatetime("date")
	embed.set_footer(text=f"Today at {time} | {date}")
	await ctx.send(embed=embed)
	await logInfo(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !test")

@bot.command(aliases=["ss", "statusset", "offline", "online"])
async def setstatus(ctx, arg):
	if ctx.author.id == 840418841942294548:
		global botStatus
		if arg in ["online", "yes", "true"]:
			botStatus = "online"
			await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="the cries of young children"))
			await ctx.send("Bot is now online")
			await logInfo(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !setstatus » Bot is now online")
		elif arg in ["offline", "false", "no"]:
			botStatus = "offline"
			await bot.change_presence(status=discord.Status.dnd, activity = discord.Activity(type=discord.ActivityType.watching, name="the world burning around me"))
			await ctx.send("Bot is now offline")
			await logInfo(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !setstatus » Bot is now offline")
	else:
		ctx.send("Insufficient Permissions")
		await logInfo(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !setstatus » Insufficient permissions")

@bot.command()
async def confess(ctx, *args):
	await ctx.message.delete()
	confession = " ".join(args)
	with open(f"serverData/{ctx.guild.id}.txt", "w+") as f:
		confessionNumber = 5
	with open(f"colourList.txt") as f:
		line = f.readlines()
	colour = str(random.choice(line))
	embed = discord.Embed(title=f"Anonymous Confession (#{confessionNumber})", description=f"\"{confession}\"", colour=discord.Colour.from_str(colour))
	time = currentDatetime("time")
	date = currentDatetime("date")
	embed.set_footer(text=f"Today at {time} | {date}")
	await ctx.send(embed=embed)
	await logInfo(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !confess » \"{confession}\"")

@bot.command(aliases=["h","helpmenu"])
async def help(ctx, *args):
	if len(args) == 0:
		embed = discord.Embed(title="Help Menu", description="""
**!calc <expr>**
Calculates simple expressions. Due to float point arithmetic limitations, results may not be accurate.

**!weather**
Shows the current weather in Sydney.

**!asx <stock_code>**
Returns graph of specified stock. Can be used on NASDAQ share codes.

**!suggest <"suggestion1"> <"suggestion 2">**
Creates a suggestion poll with reactions.

**!test**
Pings bot with blank packet.
""")

		time = currentDatetime("time")
		date = currentDatetime("date")
		embed.set_footer(text=f"Today at {time} | {date}")
		await ctx.send(embed=embed)
		await logInfo(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !help")

@bot.command(aliases=["quit", "stop", "exit"])
async def shutdown(ctx):
	if ctx.author.id == 840418841942294548:
		countdown = 5
		embed = discord.Embed(title="Shutdown Bot", description=f"Shutting down the bot in {countdown}")
		msg = await ctx.send(embed=embed)
		for i in range(countdown, -1, -1):
			embed = discord.Embed(title="Shutdown Bot", description=f"Shutting down the bot in {countdown}")
			await msg.edit(embed=embed)
			countdown = i
			await asyncio.sleep(1)
		embed = discord.Embed(title="Shutdown Bot", description=f"Bot is now offline")
		await msg.edit(embed=embed)
		await logInfo(msg=f"{ctx.message.guild} » #{ctx.message.channel} | {ctx.message.author} | !shutdown | Shutdown bot")
		await logInfo(msg="Bot has been shut down")
		sys.exit()
	else:
		await ctx.send("Insufficient Permissions")

@bot.event
async def on_botOffline(ctx):
	embed = discord.Embed(title="Bot Status", description=f"{errorStatus} Bot is currently offline")
	time = currentDatetime("time")
	date = currentDatetime("date")
	embed.set_footer(text=f"Today at {time} | {date}")
	await ctx.send(embed=embed)

async def logInfo(msg):
	log.info(msg=msg)
	time = currentDatetime("time")
	date = currentDatetime("date")

async def logError(msg):
	log.error(msg=msg)
	channel = bot.get_channel(1038017545690693702)
	time = currentDatetime("time")
	date = currentDatetime("date")

async def load_extensions():
	for filename in os.listdir("./cogs"):
		if filename.endswith(".py"):
			await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
	async with bot:
		await load_extensions()
		await logInfo("Loaded extensions")
		await bot.start(botToken)

asyncio.run(main())
