import discord
import pickle
import datetime
import time
import asyncio
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class RemindCommands(commands.Cog, name='Remind Commands'):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone='America/Los_Angeles')
        self.scheduler.start()

    async def cog_check(self, ctx):
        infile = open('storage/blacklist', 'rb')
        self.banned = pickle.load(infile)
        infile.close()
        for id in self.banned:
            if int(format(ctx.author.id)) == id:
                return False
        return True

    async def send_remind_message(self, ctx, reminder):
        await self.bot.wait_until_ready()
        await ctx.send(
            f"{ctx.message.author.mention}, I am remindering you to **{reminder}**."
        )

    @commands.command(name='remind', aliases=['rem'])
    async def remind(self, ctx, t: str, *, reminder: str = ''):
        if reminder == '':
            return await ctx.send(
                'Here\'s a reminder to tell me what to remind you about.')
        h = 0
        m = 0
        s = 0
        seconds = 0
        reminder = reminder.strip()
        if 'h' in t:
            if 'm' in t:
                h = t.split('h')[0]
                m = t.split('h')[1][:-1]
                if 's' in t:
                    h = t.split('h')[0]
                    m = t.split('h')[1].split('m')[0]
                    s = t.split('m')[1][:-1]
                else:
                    h = t.split('h')[0]
                    m = t.split('h')[1].split('m')[0]
            else:
                h = t.split('h')[0]
        elif 'm' in t:
            m = t.split('m')[0]
            if 's' in t:
                m = t.split('m')[0]
                s = t.split('m')[1][:-1]
        elif 's' in t:
            s = t.split('s')[0]
        else:
            return await ctx.send('When do I remind you?')
        try:
            seconds = int(h) * 60 * 60 + int(m) * 60 + int(s)
        except:
            return await ctx.send('Format time correctly please.')

        await ctx.send(
            f"I will remind you to **{reminder}** <t:{int(time.time())+seconds}:R>"
        )
        #t = datetime.datetime.fromtimestamp(time.time() + seconds)
        #self.scheduler.add_job(
        #    func=self.send_remind_message,
        #    trigger=CronTrigger(
        #    hour=t.strftime("%H"),
        #    minute=t.strftime("%-M"),
        #    second=t.strftime("%-S")),
        #    args=[ctx, reminder])
        await asyncio.sleep(seconds)
        await self.send_remind_message(ctx, reminder)


def setup(bot):
    bot.add_cog(RemindCommands(bot))
