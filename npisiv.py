#bot
import datetime
import os
from operator import indexOf

import discord
from discord.ext import commands
from time import sleep
import myCommands as mc
from dotenv import load_dotenv




load_dotenv()
# API Tokens
GUILD = os.getenv("DISCORD_GUILD")
TOKEN = os.getenv("DISCORD_TOKEN")

#Discord message class
message = discord.Message

# Discord context Class
context = commands.Context

# Discord Intent class
intent = discord.Intents.default()
intent.messages = True
intent.message_content = True

# Initializing bot
# bot  = discord.Client(intents=intent)
bot = commands.Bot(command_prefix="!", intents=intent)

# Default guild id
myguild = 1327148495399817227

bot_functions = ["ClassSchedule", "AssignmentSchedule"]
@bot.event
async def on_ready():
    currGuild = bot.get_guild(myguild)
    print("Logged in as a bot {0.user}".format(bot))
    print(bot.user, type(bot.user))
    print(bot.user.name, type(bot.user.name))
    print(bot.user.id, type(bot.user.id))

    print(currGuild.name)
@bot.event
async def on_message(m:message):

    username = (str)(m.author.name)
    channel = (str) (m.channel)
    content = (str) (m.content)
    print(f"From {channel} {username} says: {content}\n")

    if m.author == bot.user:
        return None

    elif content[0] == "!":
        await bot.process_commands(m)

    elif m.author != bot.user:
        if content.lower() in [str(bot.user.id), bot.user.name.lower(), "hello", "hi"]:
            sleep(.5)
            await m.channel.send(f"Hey there <@{m.author.id}>")
            # await m.channel.send(f"Hey there <@{m.author.id}>")







@bot.command()
async def ping(ctx:context):
    userid = ctx.author.id
    username = (str)(ctx.author.name)
    channel = (str) (ctx.channel)
    content = (str) (ctx.message.content)
    sleep(.4)
    # await ctx.channel.send(f"Hey there <@{ctx.author.id}>")
    await ctx.channel.send(f"I'm here <@{userid}>")

@bot.command()
async def PING(ctx: context):
    userid = ctx.author.id
    username = (str)(ctx.author.name)
    channel = (str) (ctx.channel)
    content = (str) (ctx.message.content)
    sleep(.4)
    await ctx.channel.send(f"Jeez, no need to be aggressive😒. I'm not going anywhere (at least not any time soon) <@{userid}>")

@bot.command()
async def current(ctx:context):
    await ctx.send(mc.currclass())

@bot.command()
async def next(ctx: context):
    sleep(.4)
    await ctx.send(mc.nextclass())

@bot.command()
async def list(ctx: context):
    sleep(.4)
    await ctx.send("Sure, here is a list of things i can do.\n")
    sleep(.6)
    await ctx.send(mc.commands())

bot.run(TOKEN)