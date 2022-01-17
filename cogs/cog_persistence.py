import pickle
from discord.ext import commands

class persistantCommands(commands.Cog, name='Commands that use persistence'):
  '''These are persistant commands'''
  
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

  @commands.command(name = 'daily')
  async def daily(self, ctx):
    infile = open('curr','rb')
    wallets = pickle.load(infile)
    infile.close()


def setup(bot):
	bot.add_cog(persistantCommands(bot))