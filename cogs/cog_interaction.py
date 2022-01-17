from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from collections import defaultdict

import discord
import random
import functools
import asyncio
import pickle

battle_outcomes = [
    "A meteor fell on **{loser}**, **{winner}** is left standing and has been declared the victor!",
    "**{loser}** was shot through the heart, and **{winner}** is to blame...",
    "**{winner}** has bucked **{loser}** into a tree, even Big Mac would be impressed at that kick!",
    "As they were battling, **{loser}** was struck by lightning! **{winner}** you lucked out this time!",
    "**{loser}** tried to dive at **{winner}** while fighting, somehow they missed and landed in quicksand. Try paying more attention next time **{loser}**.",
    "**{loser}** got a little... heated during the battle and ended up getting set on fire. **{winner}** wins by remaining cool.",
    "Princess Celestia came in and banished **{loser}** to the moon. Good luck getting into any battles up there!",
    "**{loser}** took an arrow to the knee, they are no longer an adventurer. Keep on adventuring **{winner}**!",
    "Common sense should make it obvious not to get into battle with **{winner}**. Apparently **{loser}** didn't get the memo...",
    "**{winner}** had a nice cup of tea with **{loser}** over their conflict, and mutually agreed that **{winner}** was Best Pony.",
    "**{winner}** and **{loser}** had an intense staring contest. Sadly, **{loser}** forgot to breathe and lost much more than the staring contest.",
    "It appears **{loser}** is actually a pacifist, they ran away screaming and crying. Maybe you should have thought of that before getting in a fight?",
    "A bunch of parasprites came in and ate up the jetpack while **{loser}** was flying with it. Those pesky critters...",
    "**{winner}** used their charm to seduce **{loser}** to surrender.",
    "**{loser}** slipped on a banana peel and fell into a pit of spikes. That's actually impressive.",
    "**{winner}** realized it was high noon, **{loser}** never even saw it coming.",
    "**{loser}** spontaneously combusted... lol rip.",
    "After many turns **{winner}** summons exodia and **{loser}** is sent to the shadow realm.",
    "**{winner}** and **{loser}** sit down for an intense game of chess, in the heat of the moment **{winner}** forgot they were playing a game and summoned a real knight...",
    "**{winner}** challenges **{loser}** to rock paper scissors, unfortunately for **{loser}**, **{winner}** chose scissors and stabbed them.",
    "**{winner}** goes back in time and becomes **{loser}**'s best friend, winning without ever throwing a punch.",
    "**{loser}** trips down some stairs on their way to the battle with **{winner}**.",
    "**{winner}** books **{loser}** a one way ticket to Flugendorf prison.",
    "**{loser}** was already dead...",
    "**{loser}** was crushed under the weight of expectations.",
    "**{loser}** was wearing a redshirt and it was their first day.",
    "**{winner}** and **{loser}** were walking along when suddenly **{loser}** got kidnapped by a flying monkey. Hope they had water with them...",
    "**{winner}** brought an army to a fist fight, **{loser}** never saw their opponent once...",
    "**{winner}** used multiple simultaneous devestating defensive deep strikes to overwhelm **{loser}**.",
    "**{winner}** and **{loser}** engage in a dance off; **{winner}** wiped the floor with **{loser}**.",
    "**{loser}** tried to hide in the sand to catch **{winner}** off guard, unfortunately looks like a Giant Antlion had the same idea for him.",
    "**{loser}** was busy playing trash videogames the night before the fight and collapsed before **{winner}**.",
    "**{winner}** threw a sick meme and **{loser}** totally got PRANK'D!",
    "**{winner}** and **{loser}** go on a skiing trip together, turns out **{loser}** forgot how to pizza french-fry.",
    "**{winner}** is the cure and **{loser}** is the disease....well **{loser}** was the disease...",
    "**{loser}** talked their mouth off at **{winner}**... literally...",
    "Looks like **{loser}** didn't put enough points into kazoo playing, who knew they would have needed it...",
    "**{loser}** was too scared by the illuminati and extra-dimensional talking horses to show up.",
    "**{loser}** didn't press x enough to not die.",
    "**{winner}** and **{loser}** go fishing to settle their debate. **{winner}** caught a sizeable fish and **{loser}** caught a boot older than time.",
    "**{winner}** did a hero landing and **{loser}** was so surprised they gave up immediately."
]

hugs = [
    "**{author}** hugs **{user}**.",
    "**{author}** tackles **{user}** for a hug.",
    "**{author}** drags **{user}**} into their dungeon where hugs ensue.",
    "**{author}** pulls **{user}** to the side for a warm hug.",
    "**{author}** goes out to buy a big enough blanket to embrace **{user}**.",
    "**{author}** hard codes an electric hug to **{user}**.",
    "**{author}** hires mercenaries to take **{user}** out....to a nice dinner.",
    "**{author}** pays $10 to not touch **{user}**.",
    "**{author}** clones themself to create a hug pile with **{user}**.",
    "**{author}** orders an airstrike of hugs **{user}**.",
    "**{author}** glomps **{user}**.",
    "**{author}** hears a knock at their door, opens it, finds **{user}** and hugs them excitedly.",
    "**{author}** goes in for a punch but misses and ends up hugging **{user}**.",
    "**{author}** hugs **{user}** from behind.",
    "**{author}** denies a hug from **{user}**.",
    "**{author}** does a hug to **{user}**.",
    "**{author}** lets **{user}** cuddle nonchalantly.",
    "**{author}** cuddles **{user}**.",
    "**{author}** burrows underground and pops up underneath **{user}** she hugs their legs.",
    "**{author}** approaches **{user}** after having gone to the gym for several months and almost crushes them.",
]


class Interaction(commands.Cog):
    """Commands that interact with another user"""

    async def cog_check(self, ctx):
      infile = open('storage/blacklist','rb')
      self.banned = pickle.load(infile)
      infile.close()
      for id in self.banned:
        if int(format(ctx.author.id)) == id:
          return False
      return True
    
    battles = defaultdict(list)
    wager = {}

    def get_receivers_battle(self, receiver):
        for battle in self.battles.get(receiver.guild.id, []):
            if battle.is_receiver(receiver):
                return battle

    def can_initiate_battle(self, player):
        for battle in self.battles.get(player.guild.id, []):
            if battle.is_initiator(player):
                return False
        return True

    def can_receive_battle(self, player):
        for battle in self.battles.get(player.guild.id, []):
            if battle.is_receiver(player):
                return False
        return True

    def start_battle(self, initiator, receiver):
        battle = Battle(initiator, receiver)
        self.battles[initiator.guild.id].append(battle)
        return battle

    def battling_off(self, battle):
        for guild, battles in self.battles.items():
            if battle in battles:
                battles.remove(battle)
                return

    def distribute_wager(self, winner, loser, wager):
          infile = open('storage/wallets','rb')
          wallets = pickle.load(infile)
          infile.close()

          balance = wallets[winner.id][0] + wager
          next = wallets[winner.id][1]
          streak = wallets[winner.id][2]
          wallet = [balance, next, streak]
          wallets[winner.id] = wallet

          balance = wallets[loser.id][0] - wager
          next = wallets[loser.id][1]
          streak = wallets[loser.id][2]
          wallet = [balance, next, streak]
          wallets[loser.id] = wallet

          outfile = open('storage/wallets','wb')
          pickle.dump(wallets,outfile)
          outfile.close()
    
    def check_wager(self, player, wager):
      infile = open('storage/wallets','rb')
      wallets = pickle.load(infile)
      infile.close()

      if wallets[player.id][0] >= wager:
        return True
      return False

    @commands.command()
    @commands.guild_only()

    async def hug(self, ctx, member: discord.Member = None):
      user = ''
      if member is None:
        messages = ['You silly goose **{}**, you cant hug nothing!', 'Ohno **{}**, do you need someone to hug? I am here for you...', '**{}**, I wish I could hug the air too...']
        await ctx.send(random.choice(messages).format(ctx.author.display_name))
      else:
        user = member.display_name
        if ctx.message.mention_everyone:
          await ctx.send("Your arms aren't big enough...")
          return
        if member.name == ctx.author.name:
          await ctx.send('I guess you can hug yourself,... :man_shrugging:')
          await asyncio.sleep(1.5)
        else:
          converter = commands.converter.MemberConverter()
          try:
            user = await converter.convert(ctx, user)
          except commands.converter.BadArgument:
            await ctx.send("Error: Could not find user: **{}**".format(member.display_name))
            return
        fmt = random.SystemRandom().choice(hugs)
        await ctx.send(fmt.format(author=ctx.author.display_name,user=user.display_name))

    @commands.command(aliases=["1v1"])
    @commands.guild_only()
    @commands.cooldown(1, 20, BucketType.user)

    async def battle(self, ctx, player2 = None, wager:int = 0):
        if ctx.message.mention_everyone:
            await ctx.send(
                "You want to battle {} people? Good luck with that...".format(
                    len(ctx.channel.members) - 1
                )
            )
            return
        if player2 is None:
            await ctx.send("Who are you trying to battle...?")
            return
        else:
            converter = commands.converter.MemberConverter()
            try:
                player2 = await converter.convert(ctx, player2)
            except commands.converter.BadArgument:
                await ctx.send("Error: Could not find user: **{}**".format(player2.name))
                return
        if ctx.author.id == player2.id:
            ctx.command.reset_cooldown(ctx)
            await ctx.send(
                "Why would you want to battle yourself? Suicide is not the answer"
            )
            return
        if ctx.bot.user.id == player2.id:
            ctx.command.reset_cooldown(ctx)
            await ctx.send("I always win, don't even try it.")
            return
        if not self.can_initiate_battle(ctx.author):
            ctx.command.reset_cooldown(ctx)
            await ctx.send("You are already battling someone!")
            return
        if not self.can_receive_battle(player2):
            ctx.command.reset_cooldown(ctx)
            await ctx.send(
                "**{}** is already being challenged to a battle!".format(player2.name)
            )
            return

        battle = self.start_battle(ctx.author, player2)

        if wager > 0:
          if self.check_wager(ctx.author, wager) is True:
            if self.check_wager(player2, wager) is True:
              fmt = (
                f"**{ctx.author.display_name}** has challenged **{player2.display_name}** to a battle for **{wager}** coins...\n"
                f"**{player2.display_name}**, `!accept` or `!decline`."
              )
            else:
              fmt = '**{}** does not have enough coins!'.format(player2.display_name)
          else:
            fmt = 'You do not have enough coins!'
        if wager <= 0:
          fmt = (
                  f"**{ctx.author.display_name}** has challenged **{player2.display_name}** to a battle...\n"
                  f"**{player2.display_name}**, `!accept` or `!decline`."
              )
        self.wager[player2.id] = wager

        part = functools.partial(self.battling_off, battle)
        ctx.bot.loop.call_later(180, part)
        await ctx.send(fmt)

    @commands.command()
    @commands.guild_only()

    async def accept(self, ctx):
        battle = self.get_receivers_battle(ctx.author)
        if battle is None:
            await ctx.send("You are not currently being challenged to a battle!")
            return

        self.battling_off(battle)

        winner, loser = battle.choose()

        fmt = random.SystemRandom().choice(battle_outcomes)
        wager = self.wager[ctx.author.id]
        await ctx.send('The battle has begun...')
        await asyncio.sleep(2)
        await ctx.send(fmt.format(winner=winner.display_name,loser=loser.display_name))
        await asyncio.sleep(1)
        if wager > 0:
          await ctx.send('**{winner}** wins **{wager}** coins from {loser}!'.format(winner=winner.display_name, wager=wager, loser=loser.display_name))
          self.distribute_wager(winner, loser, wager)

        else:
          await ctx.send('**{winner}** wins!'.format(winner=winner.display_name))


    @commands.command()
    @commands.guild_only()

    async def decline(self, ctx):
        battle = self.get_receivers_battle(ctx.author)
        if battle is None:
            await ctx.send("You are not currently being challenged to a battle!")
            return

        self.battling_off(battle)
        await ctx.send("**{}** has chickened out! What a loser...".format(ctx.author.name))


class Battle:
    async def cog_check(self, ctx):
      infile = open('storage/blacklist','rb')
      self.banned = pickle.load(infile)
      infile.close()
      for id in self.banned:
        print(id)
        if int(format(ctx.author.id)) == id:
          return False
      return True
    
    def __init__(self, initiator, receiver):
        self.initiator = initiator
        self.receiver = receiver
        self.rand = random.SystemRandom()

    def is_initiator(self, player):
        return (
            player.id == self.initiator.id
            and player.guild.id == self.initiator.guild.id
        )

    def is_receiver(self, player):
        return (
            player.id == self.receiver.id and player.guild.id == self.receiver.guild.id
        )

    def is_battling(self, player):
        return self.is_initiator(player) or self.is_receiver(player)

    def choose(self):
        """Returns the two users in the order winner, loser"""
        choices = [self.initiator, self.receiver]
        self.rand.shuffle(choices)
        return choices

def setup(bot):
    bot.add_cog(Interaction(bot))