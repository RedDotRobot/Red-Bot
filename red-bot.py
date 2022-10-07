#Import Modules
from array import array								#No idea
from ast import alias, operator						#I didn"t put that there wtf
import asyncio
from email import message_from_string
from http import client
from multiprocessing import get_context								#um
from pydoc import describe							#uh
from ssl import OPENSSL_VERSION_NUMBER				#is this a problem
import os
from turtle import color											#idfk tbh
import discord										#Discord stuff
from discord.ext import commands
from discord import FFmpegAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
from dotenv import load_dotenv						#.env
from datetime import datetime						#Datetime
import datetime as dt
import requests										#JSON Requests
import json
import mpmath										#Math shit, another problem for another day
import numpy as np
import pandas as pd
import re											#RegEx kinda pog
import yfinance as yf								#ASX lesh go
import plotly.graph_objs as go
import random										#Game maybe??? (foreshadowing)
import coloredlogs, logging

#Introduce Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, activity = discord.Activity(type=discord.ActivityType.listening, name="the cries of young children"), help_command=None)
load_dotenv()
botToken = os.getenv("botToken")
yf.pdr_override()
botStatus = "online"
botClock = "offline"

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
	if format == "timeDate":
		currentTime = datetime.now()
		formatTimeDate = currentTime.strftime("%d-%m-%Y	%H:%M:%S")
		return formatTimeDate

#Logger
logger = logging.getLogger("red-bot.py")
coloredlogs.install(level="DEBUG", fmt="%(asctime)s [%(levelname)s] %(message)s")
coloredlogs.DEFAULT_FIELD_STYLES = {
	"asctime": {"color": "black"},
	"hostname": {"color": "magenta"},
	"levelname": {"bold": True, "color": "magenta"},
	"name": {"color": "blue"},
	"programname": {"color": "cyan"}, 
	"username": {"color": "yellow"}
	}

coloredlogs.DEFAULT_LEVEL_STYLES = {
	"info": {"color": "grey"},
	"debug": {"color": "magenta"},
	"notice": {"color": "magenta"},
	"spam": {"color": "green", "faint": True},
	"success": {"bold": True, "color": "green"},
	"verbose": {"color": "blue"},
	"error": {"color": "red"},
	"warning": {"color": "yellow"},
	"critical": {"bold": True, "color": "red"}
	}

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
	if botClock == "online":
		while True:
			os.system("cls")
			print("==========================")
			print("Logged in as")
			print(bot.user.name)
			print(currentDatetime("time"))
			print("==========================")
			await asyncio.sleep(1)
	else:
		print("==========================")
		print("Logged in as")
		print(bot.user.name)
		print(currentDatetime("time"))
		print("==========================")

@bot.command(aliases=["c","calculate"])
async def calc(ctx, arg):
	equation = str(arg)
	equation = equation.replace("x", "*").replace(",", "").replace("^", "**").replace("k", "*1000").replace("m", "*1000000").replace("b", "*1000000000").replace(")(", ")*(")
	equation = equation.replace("0(", "0*(").replace("2(", "2*(").replace("3(", "3*(").replace("4(", "4*(").replace("5(", "5*(").replace("6(", "6*(").replace("7(", "7*(").replace("8(", "8*(").replace("9(", "9*(").replace(")0", ")*0").replace(")2", ")*2").replace(")3", ")*3").replace(")4", ")*4").replace(")5", ")*5").replace(")6(", ")*6").replace(")7", ")*7").replace(")8", ")*8").replace(")9", ")*9")
	result = eval(equation)
	result = f"{result:,.15f}".rstrip("0").rstrip(".")
	await ctx.send(result)
	logger.debug("did mafs")

@bot.command(aliases=["p","latency"])
async def ping(ctx):
	latency = f"{bot.latency*1000:0.2f}"
	embed=discord.Embed(title="Bot Latency", description=f"Current ping is {latency}ms".format(bot.latency*1000))
	time = currentDatetime("time")
	date = currentDatetime("date")
	embed.set_footer(text=f"Today at {time} | {date}")
	await ctx.send(embed=embed)

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
	embed.add_field(name="Weather             ㅤ", value=f"{weatherDescription}", inline=True)
	embed.add_field(name = chr(173), value = chr(173)) #Embed linebreak
	embed.add_field(name="Feels Like          ㅤ", value=f"{feelTemp}°C", inline=True)
	embed.add_field(name="Humidity            ㅤ", value=f"{humidity}%", inline=True)
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

@bot.command(aliases=["a","stock"])
async def asx(ctx, arg):
	data = yf.download(tickers=arg, period="3mo", interval="1d")
	fig = go.Figure()
	fig.add_trace(go.Candlestick(x=data.index, open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"], name = "market data"))
	arg = arg.upper()
	fig.update_layout(
		title=f"{arg} Trade Prices (3 Months)",
		yaxis_title="Stock Price (USD per Shares)")
	fig.write_image("Stock_Image/data.png")
	embed = discord.Embed(title=f"{arg} Stock Information")
	file = discord.File("Stock_Image/data.png")
	embed.set_image(url="attachment://data.png")
	time = currentDatetime("time")
	date = currentDatetime("date")
	embed.set_footer(text=f"Today at {time} | {date}")
	await ctx.send(file=file, embed=embed)

@bot.command(aliases=["delete","clear"])
async def purge(ctx, limit:int):
	if ctx.author.id == 840418841942294548:
		limit = limit + 1
		await ctx.channel.purge(limit=limit)
	else:
		await ctx.send("Insufficient permissions")

@bot.command(aliases=["servers", "serverlist"])
async def server(ctx):
	serverlist = list()
	activeservers = bot.guilds
	for guild in activeservers:
		serverlist.append(guild.name)
	await ctx.send("\n".join(map(str, serverlist)))

@bot.command(aliases=["t","status","botstatus"])
async def test(ctx):
	embed = discord.Embed(title="Bot Status", description=f"{onlineStatus} Bot is currently functional")
	time = currentDatetime("time")
	date = currentDatetime("date")
	embed.set_footer(text=f"Today at {time} | {date}")
	await ctx.send(embed=embed)

@bot.command(aliases=["ss", "statusset", "offline", "online"])
async def setstatus(ctx, arg):
	if ctx.author.id == 840418841942294548:
		global botStatus
		if arg in ["online", "yes", "true"]:
			botStatus = "online"
			await bot.change_presence(status=discord.Status.online, activity = discord.Activity(type=discord.ActivityType.listening, name="the cries of young children"))
			await ctx.send("Bot is now online")
		elif arg in ["offline", "false", "no"]:
			botStatus = "offline"
			await bot.change_presence(status=discord.Status.dnd, activity = discord.Activity(type=discord.ActivityType.watching, name="the world burning around me"))
			await ctx.send("Bot is now offline")
	else:
		ctx.send("Insufficient Permissions")

@bot.command(aliases=["h","helpmenu"])
async def help(ctx, *args):
	if len(args) == 0:
		embed = discord.Embed(title="**Help Menu**", description="List of commands. For additional assistance, contact `RedDotRobot#7360`\n\n`help`     Shows this menu\n`calc`     Simple calculator\n`weather`  Shows current weather in Sydney\n`purge`    Deletes specified number of messages\n`ping`     Outputs bot latency\n`test`     Shows if bot is currently functional\nFor additional assistance, contact `RedDotRobot#7360`")
		time = currentDatetime("time")
		date = currentDatetime("date")
		embed.set_footer(text=f"Today at {time} | {date}")
		await ctx.send(embed=embed)

@bot.event
async def on_botOffline(ctx):
	embed = discord.Embed(title="Bot Status", description=f"{errorStatus} Bot is currently offline")
	time = currentDatetime("time")
	date = currentDatetime("date")
	embed.set_footer(text=f"Today at {time} | {date}")
	await ctx.send(embed=embed)

"""async def printLog(logType, user, guild, channel, command, info):
	print("log printed breakpoint 1")
	timeDate = currentDatetime("timeDate")
	if logType == "info":
		print(f"{timeDate} [INFO] {user} {guild} => {channel} | {command} {info}")
	elif logType == "gateway":
		print(f"{timeDate} [GATEWAY] {info}")
	elif logType == "error":
		print("error has occured :(")"""

async def load_extensions():
	for filename in os.listdir("./cogs"):
		if filename.endswith(".py"):
			await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
	async with bot:
		await load_extensions()
		await bot.start(botToken)

asyncio.run(main())
