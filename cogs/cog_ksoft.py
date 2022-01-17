import discord
import pickle
import os
from discord.ext import commands
import ksoftapi

kclient = ksoftapi.Client(os.environ['KSOFT v1 TOKEN'])

class KsoftCommands(commands.Cog, name='Ksoft Api Commands'):
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

  @commands.command(name = 'lyrics', aliases=['lyric'])
  async def lyrics(self, ctx, *, query: str):
    try:
      results = await kclient.music.lyrics(query)
    except ksoftapi.NoResults:
      await ctx.send('No lyrics found for ' + query)
    else:
      first = results[0]
      s = str(first.lyrics)
      embed = discord.Embed(title="{} : {}".format(first.name, first.album), colour=discord.Colour(0x1), description=s)
      embed.set_author(name=first.artist)
      await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(KsoftCommands(bot))