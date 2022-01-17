import discord
import pickle
from discord.ext import commands


class TemplateCommands(commands.Cog, name='Template Commands'):
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

def setup(bot):
	bot.add_cog(TemplateCommands(bot))