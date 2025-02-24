import datetime
import os
import sys
import time

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

# This section listens for user messages
@bot.event
async def on_message(m:message):

    username = (str)(m.author.name)
    channel = (str) (m.channel)
    content = (str) (m.content)

    # Backend activity lol
    print(f"From {channel} {username} says: {content}\n")

    # Prevents bot recursive reply
    if m.author == bot.user:
        return None

    # Flag to separate commands from other text
    elif content[0] == "!":
        await bot.process_commands(m)

    # "Human" Messages
    elif m.author != bot.user:
        # Checks if the message is a common salutation
        if ((content.lower() in [str(bot.user.id), bot.user.name.lower(), "hello", "hi"]) or
            ("bot" in content.lower())):
            sleep(.5) # Manual delay
            await m.channel.send(f"Hey there <@{m.author.id}>") # Bot responds to the caller

        # Dont forget this here lmao
        elif content.lower() == "stop": # command to remote terminate
            sleep(5)
            sys.exit(0)


# ----------------------- Section for bot commands, see myCommands.py --------------------------#

# Basic command to verify bot presence
@bot.command()
async def ping(ctx:context):
    userid = ctx.author.id
    username = ctx.author.name
    channel = ctx.channel
    content = ctx.message.content

    sleep(.4)
    # await ctx.channel.send(f"Hey there <@{ctx.author.id}>")
    await channel.send(f"I'm here <@{userid}>") # Response to the caller

# Same as above but fun easter egg for uppercase commabd
@bot.command()
async def PING(ctx: context):
    userid = ctx.author.id
    username = ctx.author.name
    channel = ctx.channel
    content = ctx.message.content
    sleep(.4)
    await channel.send(f"Jeez, no need to be aggressive😒. I'm not going anywhere (at least not any time soon) <@{userid}>")

# Returns the current class in session
@bot.command()
async def curr(ctx:context):
    await ctx.send(mc.currclass())

# Returns the next class in session
@bot.command()
async def next(ctx: context):
    sleep(.4)
    await ctx.send(mc.nextclass())

#  Returns a list of functions the bot can perform
@bot.command()
async def list(ctx: context):
    sleep(.4)
    await ctx.send("Sure, here is a list of things i can do.\n")
    sleep(.6)
    await ctx.send(mc.commands())

# Returns a list of assignments due within a week of date invoked
@bot.command()
async def assignments(ctx: context):
    assignment = mc.assignments()
    for item in assignment:
        sleep(1)
        await ctx.send(f"{item["c_code"]} {item['a_name']} is due on {item['a_due']} by {item['a_time']}")

@bot.command()
async def duedates(ctx:context):
    await ctx.channel.send()


bot.run(TOKEN)

