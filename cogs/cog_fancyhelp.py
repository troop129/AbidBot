import discord
import discord.ext
from discord.ext import commands
from discord.ext import menus

#pip install -U git+https://github.com/Rapptz/discord-ext-menus

class fancyHelpCommands(commands.Cog, name='Fancy Help Commands'):
  '''These are the commands for the fancy help menu'''
  
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(name = 'help')
  async def help(self, ctx):
    if int(format(ctx.guild.id)) == 755833429622259913:
      pages = menus.MenuPages(source=NizamiHelp(range(1,10)), clear_reactions_after=True)
    elif int(format(ctx.guild.id)) == 811678754560016444:
      pages = menus.MenuPages(source=TRDServerHelp(range(1,14)), clear_reactions_after=True)
    else:
      pages = menus.MenuPages(source=BasicFullHelp(range(1,12)), clear_reactions_after=True)
    await pages.start(ctx)

class BasicFullHelp(menus.ListPageSource):
  def __init__(self, data):
    super().__init__(data, per_page=4)

  async def format_page(self, menu, entries):
    embedparts = [["!inspire", "!compliment <mention>", "!joke", "!nutella", "!8ball", "!choose <c1> | <c2>", "!vote <question>", "!insult <mention>", "!roast <mention>", "!yomama <mention>", "!countdown <time> <name>", "!emojify <message>", "!avatar <mention>"],
    ["Get a random inspirational quote", "Compliment someone (best if used daily)", "Random (possibly dad) joke", "NUTELLA", "It's an 8ball.", 'Separate choices with a "|"', "Brings up a vote", "Insult someone (nsfw)", "Roast someone (nsfw)", "Roast someone's mom (nsfw)", "Countdown for seconds or minutes, ex: 30s, 5m. Add optional timer name after.", "Convert your text into text-emoji-things.", "Get a user's avatar. Leave out mention to get your own."]]
    embed=discord.Embed(title="BeedoBot Help", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description="The command prefix is ! and is not changable. if you have command requests or need help, DM troop129#6666.")
    x = menu.current_page * 4
    for y in range(4):
      try:
        embed.add_field(name = embedparts[0][x], value = embedparts[1][x], inline = False)
        x += 1
      except:
        pass
    embed.set_footer(text="Page " + str(menu.current_page + 1) + " of " + str(self.get_max_pages()))
    return embed

class TRDServerHelp(menus.ListPageSource):
  def __init__(self, data):
    super().__init__(data, per_page=4)

  async def format_page(self, menu, entries):
    embedparts = [["!inspire", "!compliment <mention>", "!joke", "!nutella", "!8ball", "!choose <c1> | <c2>", "!vote <question>", "!insult <mention>", "!roast <mention>", "!yomama <mention>", "!countdown <time> <name>", "!avatar <mention>", "!emojify <message>", "!turn", "!fbi"],
    ["Get a random inspirational quote", "Compliment someone (best if used daily)", "Random (possibly dad) joke", "NUTELLA", "It's an 8ball.", 'Separate choices with a "|"', "Brings up a vote", "Insult someone (nsfw)", "Roast someone (nsfw)", "Roast someone's mom (nsfw)", "Countdown for seconds or minutes, ex: 30s, 5m. Add optional timer name after.", "Convert your text into text-emoji-things.", "Get a user's avatar. Leave out mention to get your own.", "Utility command for trd", "Returns random FBI case from API, may not work always."]]
    embed=discord.Embed(title="BeedoBot Help", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description="The command prefix is ! and is not changable. if you have command requests or need help, DM troop129#6666.")
    x = menu.current_page * 4
    for y in range(4):
      try:
        embed.add_field(name = embedparts[0][x], value = embedparts[1][x], inline = False)
        x += 1
      except:
        pass
    embed.set_footer(text="Page " + str(menu.current_page + 1) + " of " + str(self.get_max_pages()))
    return embed

class NizamiHelp(menus.ListPageSource):
  def __init__(self, data):
    super().__init__(data, per_page=4)

  async def format_page(self, menu, entries):
    embedparts = [["!inspire", "!compliment <mention>", "!joke", "!nutella", "!8ball", "!choose <c1> | <c2>", "!vote <question>", "!countdown <time> <name>", "!emojify <message>", "!avatar <mention>"],
    ["Get a random inspirational quote", "Compliment someone (best if used daily)", "Random (possibly dad) joke", "NUTELLA", "It's an 8ball.", 'Separate choices with a "|"', "Brings up a vote", "Countdown for seconds or minutes, ex: 30s, 5m. Add optional timer name after.", "Convert your text into text-emoji-things.", "Get a user's avatar. Leave out mention to get your own."]]
    embed=discord.Embed(title="BeedoBot Help", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description="The command prefix is ! and is not changable. if you have command requests or need help, DM troop129#6666.")  
    x = menu.current_page * 4
    for y in range(4):
      try:
        embed.add_field(name = embedparts[0][x], value = embedparts[1][x], inline = False)
        x += 1
      except:
        pass
    embed.set_footer(text="Page " + str(menu.current_page + 1) + " of " + str(self.get_max_pages()))
    return embed
  
def setup(bot):
	bot.add_cog(fancyHelpCommands(bot))

  @commands.command(name = 'help')
  async def help(self, ctx, *, arg = None):
    tp = 5
    if int(format(ctx.guild.id)) == 755833429622259913: #if is nizami
      tp = tp-1
    if int(format(ctx.guild.id)) == 811678754560016444: #if is trd
      tp = tp+1
    inl = False
    page = 1
    embed=discord.Embed(title="BeedoBot Help", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description="The command prefix is ! and is not changable. if you have command requests or need help, DM troop129#6666.")
    try:
      if arg != None:
        page = int(arg) 
      if page > tp:
        await ctx.send('There are only '+ str(tp) + ' pages...')
        await asyncio.sleep(2)
        await ctx.send('Idiot.')
      else:
        if page == 1 or arg == None:  
        
          embed.add_field(name="!compliment <mention>", value="Compliment someone. Best if used daily.", inline=inl)

        if page == 2:
          
        if page == 3:
          
          embed.add_field(name="!hug <mention>", value="Hug your best friend!", inline=inl)
          
        if page == 4:
          
          
        
        if page == 5:
          
          
        if page == 5:
          if int(format(ctx.guild.id)) != 755833429622259913: #not nizami
            embed.add_field(name="!insult <mention>", value="Insult someone (nsfw).", inline=inl)
            embed.add_field(name="!roast <mention>", value="Roast someone (nsfw).", inline=inl)
            embed.add_field(name="!yomama <mention>", value="Roast someone's mom.", inline=inl)
            embed.add_field(name="!urban <term>", value="Look up a word on the urban dictionary.", inline=inl)
        if page == 6:
          if int(format(ctx.guild.id)) == 811678754560016444: #TRD server
            embed.add_field(name="!turn", value="Utility command for trd.", inline=inl)
            embed.add_field(name="!trdn", value="TRD turn but not Shazzy at night.", inline=inl)
            embed.add_field(name="!fbi", value="Returns random FBI case from API.", inline=inl)
            embed.add_field(name="!chart <string>", value="What do those extra letters mean??", inline=inl)
            embed.add_field(name="!count <#>", value="See the chart values.", inline=inl)
            embed.add_field(name="!rule <#>*", value="See the TRD rules. Do `{}` for all the rules.".format('!rules'), inline=inl)
        embed.set_footer(text="A * designates optional parameters. Page "+ str(page) + ' of ' + str(tp) + '. Try "!help <#>" to go to a specific page.')
        await ctx.send(embed=embed)
    except:
      await ctx.send('Format your command correctly please.')