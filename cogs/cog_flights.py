import discord
import pickle
import os
from discord.ext import commands
import flightradar24
from datetime import datetime


class FlightCommands(commands.Cog, name='Flight Commands'):
  def __init__(self, bot):
    self.bot = bot

  async def cog_check(self, ctx):
    infile = open('storage/blacklist','rb')
    self.banned = pickle.load(infile)
    infile.close()
    for id in self.banned:
      if int(format(ctx.author.id)) == id:
        return False
    return True

  def liveFlightFinder(self, flight):
    for i in flight['result']['response']['data']:
        if i['time']['real']['arrival'] is None and i['time']['real']['departure'] is not None:
            return i
    return "NOT FOUND"
  
  def convertUnix(self, unix):
    return datetime.utcfromtimestamp(int(unix)-25200).strftime('%d-%m-%Y %I:%M %p')
  
  @commands.group(name = 'flightradar', aliases = ['fr', 'flights'], invoke_without_command = True)
  async def flightradar(self, ctx, id:str=''):
    if id == '':
      embed = discord.Embed(title="BeedoBot x FlightRadar24", colour=discord.Colour(0x1), description='Query the reams of data on flightradar24.com. Start all commands with "!flightradar".')
      embed.add_field(name="image", value="`!fr image <flight number>`", inline=True)
      await ctx.send(embed=embed)
    else:
      fr = flightradar24.Api()
      data = fr.get_flight(id)
      flight = self.liveFlightFinder(data)
      image = data['result']['response']['aircraftImages'][0]['images']['large'][1]['src']
      airline = flight['airline']['name']
      destination = flight['airport']['destination']['name']
      dcode = flight['airport']['destination']['code']['iata']
      origin = flight['airport']['origin']['name']
      ocode = flight['airport']['origin']['code']['iata']
      departure = self.convertUnix(flight['time']['real']['departure'])
      arrival = self.convertUnix(flight['time']['estimated']['arrival'])

      embed = discord.Embed(title="BeedoBot x FlightRadar24", colour=discord.Colour(0x1), description='Data on flight {}.'.format(id))
      embed.set_thumbnail(url = image)
      embed.add_field(name="Airline".format(airline), value="{}".format(airline), inline=False)
      embed.add_field(name="Origin", value="{} ({})".format(origin, ocode), inline=False)
      embed.add_field(name="Destination", value="{} ({})".format(destination, dcode), inline=False)
      embed.add_field(name="Departure", value="{}".format(departure),inline=False)
      embed.add_field(name="Arrival", value="{}".format(arrival),inline=False)
      await ctx.send(embed=embed)
  
  @flightradar.command(name = 'image', aliases = ['img'])
  async def img(self, ctx, id:str=''):
    if id == '':
      await ctx.send('I need a flight ID in order to get an image.')
    else:
      try:
        flight_id = id
        fr = flightradar24.Api()
        flight = fr.get_flight(flight_id)
        image = flight['result']['response']['aircraftImages'][0]['images']['large'][1]['src']
        await ctx.send(image)
      except:
        await ctx.send('That\'s not a real flight ID.')

def setup(bot):
	bot.add_cog(FlightCommands(bot))