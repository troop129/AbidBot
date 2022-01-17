import discord
import pickle
import requests
import pytz
import json
import datetime
from discord.ext import commands


class TwilioCommands(commands.Cog, name='Twilio Commands'):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        infile = open('storage/blacklist', 'rb')
        self.banned = pickle.load(infile)
        infile.close()
        for id in self.banned:
            if int(format(ctx.author.id)) == id:
                return False
        return ctx.author.id == self.bot.author_id

    @commands.command(name='call')
    async def call(self,
                   ctx,
                   member: discord.Member = None,
                   *,
                   message: str = ''):
        if member is None:
            return await ctx.send('I guess I\'ll call your dad...')
        if message is None:
            return await ctx.send('What do I say?')
        
        number = self.numbers[member.id]
        try:
            headers = {
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
            }
            requests.post(url,
                          params={
                              'number': number,
                              'message': message
                          },
                          headers=headers)
            await ctx.send('Ringing....')
        except:
            await ctx.send('Oops, I messed up. Can you try again?')

    @commands.command(name='callrr')
    async def callrr(self, ctx, number: int = ''):
        if number is None:
            return await ctx.send('I guess I\'ll call your dad...')
        
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
        requests.post(url, params={'number': number}, headers=headers)
        await ctx.send('Ringing....')

    @commands.command(name='alarm', alias=['schedule'])
    async def alarm(self, ctx, number: int = '', t: str = ''):
        if number == '':
            return await ctx.send('Who do I call?')
        if t == '':
            return await ctx.send('When do I call?')
        h = 0
        m = 0
        if 'h' in t:
            if 'm' in t:
                h = t.split('h')[0]
                m = t.split('h')[1][:-1]
            else:
                h = t.split('h')[0]
        elif 'm' in t:
            m = t.split('m')[0]
        ftime = datetime.datetime.now(
            pytz.timezone('US/Pacific')) + datetime.timedelta(hours=int(h),
                                                              minutes=int(m))
        
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
        try:
            r = requests.post(url,
                              params={
                                  'number': number,
                                  'time': ftime
                              },
                              headers=headers)
            data = json.loads(r.content)
            if data == 'Success!!':
                await ctx.send('I scheduled your alarm!')
            else:
                await ctx.send('I think something went wrong.')
        except:
            await ctx.send('I think I messed up. Can you try again?')


def setup(bot):
    bot.add_cog(TwilioCommands(bot))
