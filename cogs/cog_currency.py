import pickle
import random
import discord
import datetime
from discord.ext import commands

wins = [
  [
    'You won **{}** coins!',
    'Someones lucky today! You earned **{}** coins!',
    'Go buy a drink, you just won **{}** coins!'
  ],
  [
    'Get happy because you just won **{}** coins!',
    'You won **{}** coins!',
    'Can I have some of the **{}** coins you won?'
  ],
  [
    'Watch out for the gold diggers. You just won **{}** coins.',
    'I want to be you when I grow up. Because you just won **{}** coins!',
    'How does one become rich? I know, you win **{}** coins!'
  ]
]

losses = [
  [
    'You lost **{}** coins!',
    'Someones unlucky today! You lost **{}** coins!',
    'Might want to stop betting, you just lost **{}** coins!'
  ],
  [
    'Get sad because you just lost **{}** coins!',
    'You lost **{}** coins!',
    'Where you gona get back the **{}** coins you lost?'
  ],
  [
    'The gold diggers left because you just lost **{}** coins.',
    'I do not want to be you when I grow up anymore. Because you just lost **{}** coins.,Like an idiot.',
    'How does one become poor? I know, you lose **{}** coins!'
  ]
]

class currencyCommands(commands.Cog, name='Commands that use persistence'):
  '''These are currency commands'''
  def __init__(self, bot):
    self.bot = bot

  def get_wallets(self):
    infile = open('storage/wallets','rb')
    wallets = pickle.load(infile)
    infile.close()
    return wallets

  def update_wallets(self, wallets):
    outfile = open('storage/wallets','wb')
    pickle.dump(wallets,outfile)
    outfile.close()

  def update_balance(self, usr, amt):
    wallets = self.get_wallets()
    balance = wallets[usr][0] + amt
    next = wallets[usr][1]
    streak = wallets[usr][2]
    wallet = [balance, next, streak]
    wallets[usr] = wallet
    self.update_wallets(wallets)

  async def cog_check(self, ctx):
    infile = open('storage/blacklist','rb')
    self.banned = pickle.load(infile)
    infile.close()
    for id in self.banned:
      if int(format(ctx.author.id)) == id:
        return False
    wallets = self.get_wallets()
    if ctx.author.id not in wallets:
      balance = 0
      next = datetime.datetime.now()
      streak = 0
      wallet = [balance, next, streak]
      wallets[ctx.author.id] = wallet
      self.update_wallets(wallets)
    return True

  @commands.command(name = 'daily')
  async def daily(self, ctx):
    id = ctx.author.id
    wallets = self.get_wallets()
    if id in wallets:
      balance = wallets[id][0]
      next = wallets[id][1]
      streak = wallets[id][2]
    else:
      balance = 0
      next = datetime.datetime.now()
      streak = 0

    if datetime.datetime.now() > next: #if has not been claimed in 23 hours
      #if datetime.datetime.now() > next + datetime.timedelta(hours = 25): #if has been 25 hours since last claim (lose streak)
      #  streak = 1
      #  await ctx.send('Oops, you lost your streak :frowning2:.')
      #else:
      streak += 1
      daily = random.randint(50,100)+random.randint(1,3)*streak
      balance += daily
      next = datetime.datetime.now() + datetime.timedelta(hours = 23)
      wallet = [balance, next, streak]
      wallets[id] = wallet
      self.update_wallets(wallets)
      await ctx.send('Thanks for claiming your daily coins! You earned **{}** today with a streak of **{}**!'.format(daily, streak))
    else: #if time left
      timeleft = str(next - datetime.datetime.now()).split(':')
      await ctx.send(' You have **{}** hours, **{}** minutes and **{}** seconds left until you can claim again.'.format(timeleft[0], timeleft[1], timeleft[2].split('.')[0]))
    
  @commands.command(name = 'balance', aliases = ['bal'])
  async def balance(self, ctx, member: discord.Member = None):
    if member is None:
      id = ctx.author.id
    else:
      id = member.id
    wallets = self.get_wallets()
    if id in wallets:
      balance = wallets[id][0]
      if member is None:
        await ctx.send('You have a balance of **{}**.'.format(balance))
      else:
        await ctx.send('**{}** have a balance of **{}**.'.format(member.display_name, balance))
    else:
      if member is None:
        await ctx.send('You have not started collecting coins!')
      else:
        await ctx.send('**{}** has not started collecting coins.'.format(member.display_name))

  @commands.command(name='gift', aliases = ['give'])
  async def remove(self, ctx, member: discord.Member, amt:int = None):
    wallets = self.get_wallets()
    if amt == 0:
      await ctx.send("You can't give nothing!")
      return
    if amt < 0:
      await ctx.send('Naughty naughty tryna steal eh?')
      return
    if wallets[ctx.author.id][0] >= amt:
      self.update_balance(member.id, amt)
      self.update_balance(ctx.author.id, -amt)
      await ctx.send("**{}** gifted **{}** coins to **{}**. Say thanks!".format(ctx.author.display_name, str(amt), member.display_name))
    else:
      await ctx.send("You can't send **{}** coins when you only have **{}** :rolling_eyes: .".format(amt, wallets[ctx.author.id][0]))
    
  @commands.command(name='leaderboard', aliases = ['rank', 'ranks'])
  async def rank(self, ctx):
    leaderboard = {}
    wallets = self.get_wallets()
    guild = ctx.guild
    for member in guild.members:
      if member.id in wallets:
        leaderboard[member.id] = [wallets[member.id][0],member.display_name,wallets[member.id][2]]
    leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1], reverse=True))
    embed=discord.Embed(title="BeedoBot Leaderboard", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description="Yet again the capitalist mentality prevails...")
    for x in leaderboard:
      embed.add_field(name=leaderboard[x][1], value='Balance: {}, Streak: {}'.format(leaderboard[x][0], leaderboard[x][2]), inline=False)
    embed.set_footer(text="Tip: Do !daily every day to increase your streak and rewards.")
    await ctx.send(embed=embed)

  @commands.command(name='gamble', aliases=['bet'])
  async def gamble(self, ctx, amt:int):
    wallets = self.get_wallets()
    if amt == 0:
      await ctx.send("You can't bet nothing!")
      return
    if amt < 0:
      await ctx.send("You can't bet a negative amount!")
      return
    if wallets[ctx.author.id][0] >= amt:
      oc = random.randint(-3,3)
      if oc > 0:
        amt = int(oc/2*amt)
      else:
        amt = int(oc*amt/3)
      if oc != 0 and amt == 0:
        amt += 1
      if amt == 0:
        await ctx.send("RIP. You didn't win anything. On the bright side, you didn't lose anything either.")
        return
      elif amt > 0:
        fmt = random.choice(wins[oc-1])
      elif amt < 0:
        fmt = random.choice(losses[oc+1])
      self.update_balance(ctx.author.id, amt)
      await ctx.send(fmt.format(str(abs(amt))))

def setup(bot):
	bot.add_cog(currencyCommands(bot))