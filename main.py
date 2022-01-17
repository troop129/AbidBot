import os
import discord
import json
import requests
import datetime
import pytz
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)

bot.author_id = 
bot.remove_command("help")


@bot.event
async def on_ready():
    print("Logged in as " + str(bot.user))
    print("I'm in " + str(len(bot.guilds)) + " servers so far.")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name='your every command (!help)')
                              )


async def chat(payload):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
    key = os.environ.get("HUGGINGFACE_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()['generated_text']


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id in 'ids' and message.content[:1] != '!' and message.content[:1] != '*' and message.content[:-1] != '*':
        try:
            await message.channel.send(await chat(message.content))
        except:
            pass

    await bot.process_commands(message)


extensions = [
    'cogs.cog_developer', 'cogs.cog_trdserver', 'cogs.cog_general',
    'cogs.cog_tictactoe', 'cogs.cog_interaction', 'cogs.cog_help',
    'cogs.cog_currency', 'cogs.cog_ramadan', 'cogs.cog_spotify',
    'cogs.cog_flights', 'cogs.cog_twilio', 'cogs.cog_remind'
]

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)

token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)
