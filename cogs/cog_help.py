import asyncio
import discord
import discord.ext
from discord.ext import commands
import pickle

class helpCommands(commands.Cog, name='Help Server Commands'):
  '''These are the help commands for general servers'''
  
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

  @commands.group(name= 'help', invoke_without_command=True)
  async def help(self, ctx):
    embed = discord.Embed(title="BeedoBot Help Menu", colour=discord.Colour(0x1), description="Use the commands below to explore the many BeedoBot commands.", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    embed.add_field(name="Fun", value="`!help fun <#>`", inline=True)
    embed.add_field(name="Utility", value="`!help utility <#>`", inline=True)
    embed.add_field(name="Miscellaneous", value="`!help misc`", inline=True)
    embed.add_field(name="Interaction", value="`!help interaction`", inline=True)
    embed.add_field(name="Currency", value="`!help currency`", inline=True)
    if int(format(ctx.guild.id)) == 755833429622259913:
      embed.add_field(name="Ramadan", value='`!help ramadan`')
    if int(format(ctx.guild.id)) == 811678754560016444:
      embed.add_field(name="TRD", value='`!help trd`')
    embed.set_footer(text='The help menu is stil being rewritten at this time. Thank you for your patience.')
    await ctx.send(embed=embed)

  @help.command(name="fun")
  async def fun(self, ctx, arg:int = 1):
    inl = False
    pages = 2
    embed = discord.Embed(title="BeedoBot Fun Commands", colour=discord.Colour(0x1), description="BeedoBot loves to have fun.", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    if arg == 0 or arg == 1:
      embed.add_field(name="!joke", value="Random (possibly dad) joke.", inline=inl)
      embed.add_field(name="!nutella", value="NUTELLA!", inline=inl)
      embed.add_field(name="!emojify <message>", value="Convert your text into text-emoji-things.", inline=inl)
      embed.add_field(name="!avatar <mention>*", value="Get a user's avatar. Leave out mention to get your own.", inline=inl)
      embed.add_field(name="!clap <message>", value="Puts clap emojis between your words. For extra emphasis, you know?", inline=inl)
      embed.set_footer(text='Page 1 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
    elif arg == 2:
      embed.add_field(name="!inspire", value="Get a random inspirational quote.", inline=inl)
      embed.add_field(name="!f", value="Can I get an F in the chat?", inline=inl)
      embed.add_field(name="!echo <channel>* <message>", value="Echoes your message in the channel of your choice. Leave out channel paramter for echo in same channel.", inline=inl)
      embed.add_field(name="!sarcasm <phrase>", value="tHiS CoMmAnD iS tHe BeSt!", inline=inl)
      embed.add_field(name="!randomsong", value="Get a random song from Spotify.")
      embed.set_footer(text='Page 2 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
    if arg > pages or arg < 1:
      await ctx.send('There is no page {} you silly goose!'.format(arg))
    else:
      await ctx.send(embed=embed)
  
  @help.command(name="utility")
  async def utility(self, ctx, arg:int = 1):
    inl = False
    pages = 2
    embed = discord.Embed(title="BeedoBot Utility Commands", colour=discord.Colour(0x1), description="BeedoBot can be very helpful to you.", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    if arg == 0 or arg == 1:
      embed.add_field(name="!choose <c1> | <c2>", value='Seperate choices with a "|" please.', inline=inl)
      embed.add_field(name="!countdown <time> <name>*", value="Countdown for seconds or minutes, ex: 30s, 5m. Add optional timer name after for organization.", inline=inl)
      embed.add_field(name="!vote <question>", value="Brings up a vote...", inline=inl)
      embed.add_field(name="!poll <p1> | <p2>", value="Starts a poll, can have up to 9 options.", inline=inl)
      embed.add_field(name="!search <parameter>", value="Search bing for whatever term you like (writing a google api atm).", inline=inl)
      embed.set_footer(text='Page 1 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
    elif arg == 2:
      embed.add_field(name="!define <word>", value="Returns the Oxford Dictionary's definition of a word.", inline=inl)
      embed.add_field(name="!coinflip", value="Flip a coin!", inline=inl)
      embed.add_field(name="!8ball", value="It's an 8ball.", inline=inl)
      embed.add_field(name="!randomnumber <#> <#>", value="Returns a random integer between the two value parameters (inclusive).", inline=inl)
      embed.set_footer(text='Page 2 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
    if arg > pages or arg < 1:
      await ctx.send('There is no page {} you silly goose!'.format(arg))
    else:
      await ctx.send(embed=embed)

  @help.command(name="misc", aliases=['miscellaneous'])
  async def misc(self, ctx, arg:int = 1):
    inl = False
    pages = 2
    embed = discord.Embed(title="BeedoBot Miscellaneous Commands", colour=discord.Colour(0x1), description="Commands that don't fit in other categories.", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    if arg == 0 or arg == 1:
      
      embed.set_footer(text='Page 1 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
    elif arg == 2:
          
      embed.set_footer(text='Page 2 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
    if arg > pages or arg < 1:
      await ctx.send('There is no page {} you silly goose!'.format(arg))
    else:
      await ctx.send(embed=embed)
  
  @help.command(name='interaction', aliases=['games', 'game'])
  async def interaction(self, ctx, arg:int = 1):
    inl = False
    pages = 1
    embed = discord.Embed(title="BeedoBot Games Commands", colour=discord.Colour(0x1), description="BeedoBot loves to play...", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    if arg == 0 or arg == 1:
      embed.add_field(name="!challenge <mention>", value="Start a tictactoe game with a friend! Still in development...", inline=inl)
      embed.add_field(name="!battle <mention>", value="Start a battle with a friend!", inline=inl)
      embed.set_footer(text='Page 1 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
      embed.add_field(name="!compliment <mention>", value="Compliment someone. Best if used daily.", inline=inl)
    #elif arg == 2:
      
    #  embed.set_footer(text='Page 2 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
    if arg > pages or arg < 1:
      await ctx.send('There is no page {} you silly goose!'.format(arg))
    else:
      await ctx.send(embed=embed)

  @help.command(name='currency', aliases=['curr'])
  async def currency(self, ctx, arg:int = 1):
    inl = False
    pages = 2
    embed = discord.Embed(title="BeedoBot Currency Commands", colour=discord.Colour(0x1), description="Currency commands are still under development.", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    if arg == 0 or arg == 1:
      embed.add_field(name="!daily", value="Claim your daily coins.", inline=inl)
      embed.add_field(name="!balance", value="View the richest people in the server.", inline=inl)
      embed.add_field(name="!gift <mention> <amount>", value="Send a poor person some funds.", inline=inl)
      embed.add_field(name="!bet <wager>", value="A chance to win some cash...", inline=inl)
      embed.set_footer(text='Page 1 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
    elif arg == 2:
      embed.add_field(name="!leaderboard", value="View the richest people in the server.", inline=inl)
      embed.add_field(name="!battle <mention> <wager>*", value="Have a battle with someone, and win coins!", inline=inl)
      embed.set_footer(text='Page 2 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
    if arg > pages or arg < 1:
      await ctx.send('There is no page {} you silly goose!'.format(arg))
    else:
      await ctx.send(embed=embed)

  @help.command(name='ramadan', aliases=['islamic', 'islam'])
  async def ramadan(self, ctx, arg:int = 1):
    if int(format(ctx.guild.id)) == 755833429622259913:
      inl = False
      pages = 1
      embed = discord.Embed(title="BeedoBot Ramadan Commands", colour=discord.Colour(0x1), description="Ramadan Mubararak!", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
      if arg == 0 or arg == 1:
        embed.add_field(name="!prayertimes <MM/DD/YYYY>*", value="Lists the prayer times for the date, leave out to get todays.", inline=inl)
        embed.add_field(name="!pt <prayer>", value="See when a specific prayer or event (iftaar/suhoor) is.", inline=inl)
        embed.add_field(name="!setlocation <city>", value="Change your location for the prayer time calculation", inline=inl)
        embed.set_footer(text='Page 1 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
      if arg > pages or arg < 1:
        await ctx.send('There is no page {} you silly goose!'.format(arg))
      else:
        await ctx.send(embed=embed)

  @help.command(name='trd')
  async def trd(self, ctx, arg:int = 1):
    if int(format(ctx.guild.id)) == 811678754560016444 or int(format(ctx.guild.id)) == 537475171838328838 : 
      inl = False
      pages = 1
      embed = discord.Embed(title="BeedoBot TRD Server Commands", colour=discord.Colour(0x1), description="Special commands just for you guys.", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
      if arg == 0 or arg == 1:
        embed.add_field(name="!turn", value="Utility command for trd.", inline=inl)
        embed.add_field(name="!fbi", value="Returns random FBI case from API.", inline=inl)
        embed.add_field(name="!chart <string>", value="What do those extra letters mean??", inline=inl)
        embed.add_field(name="!count <#>", value="See the chart values.", inline=inl)
        embed.add_field(name="!rule <#>*", value="See the TRD rules. Do `{}` for all the rules.".format('!rules'), inline=inl)
        embed.set_footer(text='Page 1 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
      elif arg == 2:
        embed.add_field(name="!rule <#>*", value="See the TRD rules. Do `{}` for all the rules.".format('!rules'), inline=inl)
        embed.add_field(name="![name]time*", value="Replace [name] with the name of the person whose time you want to know.".format('!rules'), inline=inl)
        embed.set_footer(text='Page 2 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
      if arg > pages or arg < 1:
        await ctx.send('There is no page {} you silly goose!'.format(arg))
      else:
        await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(helpCommands(bot)) 