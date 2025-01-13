#bot
import os
import discord
from discord.ext import commands
from time import sleep


from dotenv import load_dotenv

load_dotenv()
# API Tokens
GUILD = os.getenv("DISCORD_GUILD")
TOKEN = os.getenv("DISCORD_TOKEN")

#Discord message class
message = discord.Message

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

@bot.command()
async def ping(ctx:context):
    username = (str)(ctx.author.name)
    channel = (str) (ctx.channel)
    content = (str) (ctx.message.content)
    sleep(.4)
    # await ctx.channel.send(f"Hey there <@{ctx.author.id}>")
    await ctx.channel.send(f"Hey there")



bot.run(TOKEN)