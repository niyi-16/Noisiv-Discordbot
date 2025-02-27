import datetime
import os
import sys
import time
from io import BytesIO

import discord
from discord.ext import commands
from discord import app_commands
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

# Default guild id
myguild = 1327148495399817227

class Noisiv(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intent)

    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=discord.Object(id=myguild))
        await self.tree.sync()

bot = Noisiv()

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

# Same as above but fun easter egg for uppercase command
@bot.command()
async def PING(ctx: context):
    userid = ctx.author.id
    username = ctx.author.name
    channel = ctx.channel
    content = ctx.message.content
    sleep(.4)
    await channel.send(f"Jeez, no need to be aggressive😒. I'm not going anywhere (at least not any time soon) <@{userid}>")

# Returns the current class in session
@bot.tree.command(name="curr", description="Returns the current class in session")
async def curr(interaction: discord.Interaction):
    await interaction.response.send_message(mc.currclass())

# Returns the next class in session
@bot.tree.command(name="next", description="Returns the next class in session")
async def next(interaction: discord.Interaction):
    sleep(.4)
    await interaction.response.send_message(mc.nextclass())

#  Returns a list of functions the bot can perform
@bot.tree.command(name="list", description="Returns a list of functions the bot can perform")
async def list(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    sleep(.4)
    await interaction.edit_original_response(content="Sure, here is a list of things i can do.\n")
    sleep(.6)

    commands_list = [f"{command["command"]} - {command["description"]}" for command in mc.bot_functions_call]
    await interaction.edit_original_response(content="\n".join(commands_list))

# Returns a list of assignments due within a week of date invoked
@bot.tree.command(name="assignments", description="Returns a list of assignments due within a week of date invoked")
async def assignments(interaction: discord.Interaction):
    assignment = mc.assignments()

    if len(assignment) == 0:
        await interaction.response.send_message("No assignments coming up this week")
    else:
        assignment_list = [
           f"{item["c_code"]} {item['a_name']} is due on {item['a_due']} by {item['a_time']}"
                          for item in assignment
        ]
        response_message = "\n".join(assignment_list)
        await interaction.response.send_message(response_message)

@bot.tree.command(name="tests", description="Returns a list of tests due within a week of date invoked")
async def tests(interaction: discord.Interaction):
    test = mc.tests()

    if len(test) == 0:
        await interaction.response.send_message("No tests coming up this week")

    else:
        test_list = [f"{item['c_code']} {item['t_name']} is due on {item['t_due']} by {item['t_time']}" for item in test]
        response_message = "\n".join(test_list)
        await interaction.response.send_message(response_message)

@bot.tree.command(name="courses", description="Returns a list of courses for the current semester")
async def courses(interaction: discord.Interaction):
    # get courses
    courses = mc.courses()

    # format and store in list
    course_list =  [f"{item['c_code']} - {item['name']}" for item in courses]

    # format response
    response_message = "\n".join(course_list)
    await interaction.response.send_message(response_message)

@bot.tree.command(name="duedates", description="Returns a list of all due dates for the rest of the semester")
async def duedates(interaction: discord.Interaction):
    due_dates = mc.duedates()

    if len(due_dates) == 0:
       await interaction.response.send_message("No due dates coming up this semester")

    else:
        # dues = [f"{item['code_name']} - {item['name']} is due {item["due"]} by {item["time"]}" for item in due_dates]
        response_message = format_as_table(due_dates)

        file = discord.File(
            BytesIO(response_message.encode()),
            filename="due_dates.txt"
        )

        await interaction.response.send_message(file=file)
        # await interaction.response.send_message(response_message)

@bot.tree.command(name="remind", description="Reminds you of something")
async def remind(interaction: discord.Interaction):
    await interaction.response.send_message("I will remind you of something")


def format_as_table(msg):
    """
   Formats due dates into an evenly spaced text table.
   """

    if not msg:
        return "No due dates found."

        # Convert all rows to strings first
    rows = [
        [
            str(item["code_name"]),
            str(item["name"]),
            str(item["due"]),
            str(item["time"]),
        ]
        for item in msg
    ]

    headers = ["Course", "Assignment", "Due Date", "Time"]

    # Determine max width for each column
    col_widths = []

    for i in range(len(headers)):
        max_width = len(headers[i])

        for row in rows:
            max_width = max(max_width, len(row[i]))

        col_widths.append(max_width)

    # Helper function to format a row
    def format_row(row):
        return " | ".join(
            row[i].ljust(col_widths[i])
            for i in range(len(row))
        )

    # Build table
    lines = []

    # Header
    lines.append(format_row(headers))

    # Separator
    separator = "-+-".join(
        "-" * width for width in col_widths
    )
    lines.append(separator)

    # Data rows
    for row in rows:
        lines.append(format_row(row))

    return "\n".join(lines)

bot.run(TOKEN)

