import discord
import pickle
from discord.ext import commands

class DevCommands(commands.Cog, name='Developer Commands'):
  def __init__(self, bot):
    self.bot = bot

  async def cog_check(self, ctx):
    return ctx.author.id == self.bot.author_id

  @commands.command(name = 'reload', aliases = ['rl'])
  async def reload(self, ctx, cog):
    extensions = self.bot.extensions
    if cog == 'all':
      for extension in extensions:
        self.bot.unload_extensions(cog)
        self.bot.load_extension(cog)
        await ctx.send('Done!')
    if cog in extensions:
      self.bot.unload_extension(cog)
      self.bot.load_extension(cog)
      await ctx.send('Done!')
    else:
      await ctx.send('Unknown Cog')
    
  @commands.command(name = 'unload', aliases = ['ul'])
  async def unload(self, ctx, cog):
    extensions = self.bot.extensions
    if cog not in extensions:
      await ctx.send("Cog is not loaded!")
      return
    self.bot.unload_extension(cog)
    await ctx.send(f"`{cog}` has successfully been unloaded.")
  
  @commands.command(name = 'listcogs', aliases = ['lc'])
  async def load(self, ctx):
    base_string = "```css\n"
    base_string += "\n".join([str(cog) for cog in self.bot.extensions])
    base_string += "\n```"
    await ctx.send(base_string)
	
  '''
  @commands.command(name='setupblacklist')
  async def setupblacklist(self, ctx):
    data = []
    outfile = open('storage/blacklist','wb')
    pickle.dump(data,outfile)
    outfile.close()
    await ctx.send('Blacklist has been setup.')
  '''
  
  @commands.command(name='blacklist', aliases=['bl'])
  async def blacklist(self, ctx, member: discord.Member):
    infile = open('storage/blacklist','rb')
    data = pickle.load(infile)
    infile.close()

    if member.id not in data:
      data.append(member.id)
      outfile = open('storage/blacklist','wb')
      pickle.dump(data,outfile)
      outfile.close()
      await ctx.send('**{}** is now blacklisted.'.format(member.display_name))
    else:
      await ctx.send('**{}** is already blacklisted.'.format(member.display_name))

  @commands.command(name='whitelist', aliases=['wl'])
  async def whitelist(self, ctx, member: discord.Member):
    infile = open('storage/blacklist','rb')
    data = pickle.load(infile)
    infile.close()

    if member.id in data:
      data.remove(member.id)
      outfile = open('storage/blacklist','wb')
      pickle.dump(data,outfile)
      outfile.close()
      await ctx.send('**{}** is now whitelisted.'.format(member.display_name))
    else:
      await ctx.send('**{}** was not in the blacklist before.'.format(member.display_name))
  
  @commands.command(name='grant')
  async def grant(self, ctx, member: discord.Member, amt:int):
    infile = open('storage/wallets','rb')
    wallets = pickle.load(infile)
    infile.close()

    balance = wallets[member.id][0] + amt
    next = wallets[member.id][1]
    streak = wallets[member.id][2]
    wallet = [balance, next, streak]
    wallets[member.id] = wallet

    outfile = open('storage/wallets','wb')
    pickle.dump(wallets,outfile)
    outfile.close()

    await ctx.send("Granted **{}** coins to **{}**. Yes you're welcome.".format(str(amt), member.display_name))

  @commands.command(name='remove')
  async def remove(self, ctx, member: discord.Member, amt:int):
    infile = open('storage/wallets','rb')
    wallets = pickle.load(infile)
    infile.close()

    balance = wallets[member.id][0] - amt
    next = wallets[member.id][1]
    streak = wallets[member.id][2]
    wallet = [balance, next, streak]
    wallets[member.id] = wallet

    outfile = open('storage/wallets','wb')
    pickle.dump(wallets,outfile)
    outfile.close()

    await ctx.send("Removed **{}** coins from **{}**. RIP.".format(str(amt), member.display_name))

  @commands.command(name = 'talk')
  async def talk(self, ctx):
    while True:
      msg = await self.bot.wait_for("message")
      if msg.content != 'EXIT':
        await discord.utils.get(self.bot.guilds[0].text_channels, name='general').send(msg.content)
      else:
        break

  @commands.command(name = 'talkj')
  async def talkj(self, ctx):
    j = await self.bot.fetch_user(420069514399580171)
    while True:
      #msg = await self.bot.wait_for("message")
      #if msg.content != 'EXIT':
      #  await j.send(msg.content)
      m = input()
      if m != 'EXIT':
        await j.send(m)
      else:
        break

  @commands.command(name = 'talks')
  async def talks(self, ctx):
    s = await self.bot.fetch_user(452630630635798528)
    await ctx.send('starting')
    while True:
      #msg = await self.bot.wait_for("message")
      #if msg.content != 'EXIT':
      #  await j.send(msg.content)
      m = input()
      if m != 'EXIT':
        await s.send(m)
      else:
        break
        print('broken')

  @commands.command(name = 'talka')
  async def talka(self, ctx):
    a = await self.bot.fetch_user(319057455529197568)
    await ctx.send('starting')
    while True:
      #msg = await self.bot.wait_for("message")
      #if msg.content != 'EXIT':
      #  await j.send(msg.content)
      m = input()
      if m != 'EXIT':
        await a.send(m)
      else:
        break
        print('broken')

def setup(bot):
	bot.add_cog(DevCommands(bot))