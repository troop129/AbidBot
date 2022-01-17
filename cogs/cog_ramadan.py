import requests
import json
import discord
import pickle
import http.client
import urllib.parse
import datetime
from pytz import timezone
from discord.ext import commands


class trdCommands(commands.Cog, name='TRD Server Commands'):
    '''These are the commands for the TRD server'''
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        infile = open('storage/blacklist', 'rb')
        self.banned = pickle.load(infile)
        infile.close()
        for id in self.banned:
            if int(format(ctx.author.id)) == id:
                return False
        return int(
            format(ctx.guild.id)
        ) == 755833429622259913 or ctx.author.id == self.bot.author_id

    def ctime(self, time):
        return datetime.datetime.strptime(time, "%H:%M").strftime("%I:%M %p")

    def get_location(self):
        infile = open('storage/locations', 'rb')
        locations = pickle.load(infile)
        infile.close()
        return locations

    def update_location(self, locations):
        outfile = open('storage/locations', 'wb')
        pickle.dump(locations, outfile)
        outfile.close()

    def get_lat_long(self, location):
        conn = http.client.HTTPConnection('api.positionstack.com')
        params = urllib.parse.urlencode({
            'query': location
        })
        conn.request('GET', '/v1/forward?{}'.format(params))
        res = conn.getresponse()
        data = res.read()
        return data.decode().split('"latitude":')[1].split(',')[
            0] + ',' + data.decode().split('"longitude":')[1].split(',')[0]

    def get_timezone(self, lat, lng):
        url = "http://api.timezonedb.com/v2.1/get-time-zone?&format=json&by=position&lat={}&lng={}".format(
            lat, lng)
        response = requests.request("GET", url)
        data = json.loads(response.content)
        return data['zoneName']

    def timeuntil(self, begin, tz):
        hour, minute = map(int, begin.split(':'))
        now = datetime.datetime.now(timezone(tz)).replace(tzinfo=None)
        future = datetime.datetime(now.year, now.month, now.day, hour, minute)
        return str(future - now).split(':')

    def get_ptime(self, day, lat, long):
        url = ('http://api.aladhan.com/v1/timings'
               '/' + day + '?latitude={}'.format(lat) +
               '&longitude={}'.format(long) + '&method=2')
        pt = []
        payload = requests.get(url).json()
        for k in payload['data']['timings'].values():
            pt.append(k)
        return pt

    def get_ptime_roseville(self, day):
        url = ('http://api.aladhan.com/v1/timings'
               '/' + day + '?latitude=38.80160586408448'
               '&longitude=-121.31378519625713'
               '&method=2')
        pt = []
        payload = requests.get(url).json()
        for k in payload['data']['timings'].values():
            pt.append(k)
        return pt

    def get_ptimes_array(self, ctx, day):
        locations = self.get_location()
        if ctx.author.id in locations:
            lat = locations[ctx.author.id][0]
            long = locations[ctx.author.id][1]
            day = datetime.datetime.now(timezone(
                locations[ctx.author.id][3])).strftime("%d-%m-%Y")
            pt = self.get_ptime(day, lat, long)
        else:
            day = datetime.datetime.now(
                timezone('US/Pacific')).strftime("%d-%m-%Y")
            pt = self.get_ptime_roseville(day)
        times = {}
        times['fajr'] = pt[0]
        times['sunrise'] = pt[1]
        times['dhuhr'] = pt[2]
        times['asr'] = pt[3]
        times['maghrib'] = pt[4]
        times['sunset'] = pt[5]
        times['isha'] = pt[6]
        times['iftaar'] = pt[4]
        times['iftar'] = pt[4]
        times['suhoor'] = pt[0]
        return times

    @commands.group(name='pt',
                    aliases=['prayertimes', 'prayertime', 'whenis', 'wi'],
                    invoke_without_command=True)
    async def pt(self, ctx, day: str = None):
        if day is None:
            day = datetime.datetime.today().strftime("%d-%m-%Y")
            name = 'today'
        else:
            try:
                day = datetime.datetime.strptime(
                    day, "%m/%d/%Y").strftime("%d-%m-%Y")
                name = datetime.datetime.strptime(
                    day, "%d-%m-%Y").strftime("%a, %B %d %Y")
            except:
                await ctx.send('Please format the date correctly: `MM/DD/YYYY`'
                               )
                return
        locations = self.get_location()
        if ctx.author.id in locations:
            lat = locations[ctx.author.id][0]
            long = locations[ctx.author.id][1]
            day = datetime.datetime.now(timezone(
                locations[ctx.author.id][3])).strftime("%d-%m-%Y")
            pt = self.get_ptime(day, lat, long)
            embed = discord.Embed(
                title="BeedoBot Prayer Times",
                description="Prayer times in **{}** from the *aladhan.com* API."
                .format(locations[ctx.author.id][2]))
        else:
            day = datetime.datetime.now(
                timezone('US/Pacific')).strftime("%d-%m-%Y")
            pt = self.get_ptime_roseville(day)
            embed = discord.Embed(
                title="BeedoBot Prayer Times",
                description=
                "Prayer times in Roseville, CA, from the *aladhan.com* API.")
        fajr = self.ctime(pt[0])
        sunrise = self.ctime(pt[1])
        dhuhr = self.ctime(pt[2])
        asr = self.ctime(pt[3])
        maghrib = self.ctime(pt[4])
        sunset = self.ctime(pt[5])
        isha = self.ctime(pt[6])
        embed.add_field(
            name="Prayer times for {}:".format(name),
            value=
            "Fajr: **{}**\n Dhuhr: **{}**\n Asr: **{}**\n Maghrib: **{}**\n Isha: **{}**"
            .format(fajr, dhuhr, asr, maghrib, isha))
        await ctx.send(embed=embed)

    @pt.command(name='fajr', aliases=['suhoor'])
    async def fajr(self, ctx, day: str = None):
        if day is None:
            day = datetime.datetime.today().strftime("%d-%m-%Y")
            name = 'today'
        else:
            try:
                day = datetime.datetime.strptime(
                    day, "%m/%d/%Y").strftime("%d-%m-%Y")
                name = "on **{}**".format(
                    datetime.datetime.strptime(
                        day, "%d-%m-%Y").strftime("%a, %B %d %Y"))
            except:
                await ctx.send('Please format the date correctly: `MM/DD/YYYY`'
                               )
                return
        locations = self.get_location()
        if ctx.author.id in locations:
            lat = locations[ctx.author.id][0]
            long = locations[ctx.author.id][1]
            loc = locations[ctx.author.id][2]
            day = datetime.datetime.now(timezone(
                locations[ctx.author.id][3])).strftime("%d-%m-%Y")
            pt = self.get_ptime(day, lat, long)
        else:
            day = datetime.datetime.now(
                timezone('US/Pacific')).strftime("%d-%m-%Y")
            pt = self.get_ptime_roseville(day)
            loc = 'Roseville'
        fajr = self.ctime(pt[0])
        await ctx.send('Fajr is at **{}** {} in **{}**.'.format(
            fajr, name, loc))

    @pt.command(name='dhuhr')
    async def dhuhr(self, ctx, day: str = None):
        if day is None:
            day = datetime.datetime.today().strftime("%d-%m-%Y")
            name = 'today'
        else:
            try:
                day = datetime.datetime.strptime(
                    day, "%m/%d/%Y").strftime("%d-%m-%Y")
                name = "on **{}**".format(
                    datetime.datetime.strptime(
                        day, "%d-%m-%Y").strftime("%a, %B %d %Y"))
            except:
                await ctx.send('Please format the date correctly: `MM/DD/YYYY`'
                               )
                return
        locations = self.get_location()
        if ctx.author.id in locations:
            lat = locations[ctx.author.id][0]
            long = locations[ctx.author.id][1]
            loc = locations[ctx.author.id][2]
            day = datetime.datetime.now(timezone(
                locations[ctx.author.id][3])).strftime("%d-%m-%Y")
            pt = self.get_ptime(day, lat, long)
        else:
            day = datetime.datetime.now(
                timezone('US/Pacific')).strftime("%d-%m-%Y")
            pt = self.get_ptime_roseville(day)
            loc = 'Roseville'
        dhuhr = self.ctime(pt[2])
        await ctx.send('Dhuhr is at **{}** {} in **{}**.'.format(
            dhuhr, name, loc))

    @pt.command(name='asr')
    async def asr(self, ctx, day: str = None):
        if day is None:
            day = datetime.datetime.today().strftime("%d-%m-%Y")
            name = 'today'
        else:
            try:
                day = datetime.datetime.strptime(
                    day, "%m/%d/%Y").strftime("%d-%m-%Y")
                name = "on **{}**".format(
                    datetime.datetime.strptime(
                        day, "%d-%m-%Y").strftime("%a, %B %d %Y"))
            except:
                await ctx.send('Please format the date correctly: `MM/DD/YYYY`'
                               )
                return
        locations = self.get_location()
        if ctx.author.id in locations:
            lat = locations[ctx.author.id][0]
            long = locations[ctx.author.id][1]
            loc = locations[ctx.author.id][2]
            day = datetime.datetime.now(timezone(
                locations[ctx.author.id][3])).strftime("%d-%m-%Y")
            pt = self.get_ptime(day, lat, long)
        else:
            day = datetime.datetime.now(
                timezone('US/Pacific')).strftime("%d-%m-%Y")
            pt = self.get_ptime_roseville(day)
            loc = 'Roseville'
        asr = self.ctime(pt[3])
        await ctx.send('Asr is at **{}** {} in **{}**.'.format(asr, name, loc))

    @pt.command(name='maghrib', aliases=['iftaar'])
    async def maghrib(self, ctx, day: str = None):
        if day is None:
            day = datetime.datetime.today().strftime("%d-%m-%Y")
            name = 'today'
        else:
            try:
                day = datetime.datetime.strptime(
                    day, "%m/%d/%Y").strftime("%d-%m-%Y")
                name = "on **{}**".format(
                    datetime.datetime.strptime(
                        day, "%d-%m-%Y").strftime("%a, %B %d %Y"))
            except:
                await ctx.send('Please format the date correctly: `MM/DD/YYYY`'
                               )
                return
        locations = self.get_location()
        if ctx.author.id in locations:
            lat = locations[ctx.author.id][0]
            long = locations[ctx.author.id][1]
            loc = locations[ctx.author.id][2]
            day = datetime.datetime.now(timezone(
                locations[ctx.author.id][3])).strftime("%d-%m-%Y")
            pt = self.get_ptime(day, lat, long)
        else:
            day = datetime.datetime.now(
                timezone('US/Pacific')).strftime("%d-%m-%Y")
            pt = self.get_ptime_roseville(day)
            loc = 'Roseville'
        maghrib = self.ctime(pt[4])
        await ctx.send('Maghrib is at **{}** {} in **{}**.'.format(
            maghrib, name, loc))

    @pt.command(name='isha')
    async def isha(self, ctx, day: str = None):
        if day is None:
            day = datetime.datetime.today().strftime("%d-%m-%Y")
            name = 'today'
        else:
            try:
                day = datetime.datetime.strptime(
                    day, "%m/%d/%Y").strftime("%d-%m-%Y")
                name = "on **{}**".format(
                    datetime.datetime.strptime(
                        day, "%d-%m-%Y").strftime("%a, %B %d %Y"))
            except:
                await ctx.send('Please format the date correctly: `MM/DD/YYYY`'
                               )
                return
        locations = self.get_location()
        if ctx.author.id in locations:
            lat = locations[ctx.author.id][0]
            long = locations[ctx.author.id][1]
            loc = locations[ctx.author.id][2]
            day = datetime.datetime.now(timezone(
                locations[ctx.author.id][3])).strftime("%d-%m-%Y")
            pt = self.get_ptime(day, lat, long)
        else:
            day = datetime.datetime.now(
                timezone('US/Pacific')).strftime("%d-%m-%Y")
            pt = self.get_ptime_roseville(day)
            loc = 'Roseville'
        isha = self.ctime(pt[6])
        await ctx.send('Isha is at **{}** {} in **{}**.'.format(
            isha, name, loc))

    @commands.command(name='tu', aliases=['timeuntil'])
    async def tu(self, ctx, prayer: str = None):
        if prayer is None:
            await ctx.send('To when do I calculate? Try `!timeuntil maghrib`')
            return
        locations = self.get_location()
        if ctx.author.id in locations:
            day = datetime.datetime.now(timezone(
                locations[ctx.author.id][3])).strftime("%d-%m-%Y")
        else:
            day = datetime.datetime.now(
                timezone('US/Pacific')).strftime("%d-%m-%Y")
        times = self.get_ptimes_array(ctx, day)
        if prayer in times:
            if ctx.author.id in locations:
                tu = self.timeuntil(str(times[prayer]),
                                    locations[ctx.author.id][3])
            else:
                tu = self.timeuntil(times[prayer], 'US/Pacific')
            if tu[0].isnumeric():
                await ctx.send(
                    '**{}** is **{}** hours and **{}** minutes away.'.format(
                        prayer, tu[0], tu[1]))
            else:
                if ctx.author.id in locations:
                    day = (datetime.datetime.now(
                        timezone(locations[ctx.author.id][3])) +
                           datetime.timedelta(days=1)).strftime("%d-%m-%Y")
                    day1 = datetime.datetime.now(
                        timezone(
                            locations[ctx.author.id][3])).strftime("%d-%m-%Y")
                    times = self.get_ptimes_array(ctx, day)
                    tu = self.timeuntil(str(times[prayer]),
                                        locations[ctx.author.id][3])
                else:
                    day = (datetime.datetime.now(timezone('US/Pacific')) +
                           datetime.datetime.timedelta(days=1)
                           ).strftime("%d-%m-%Y")
                    times = self.get_ptimes_array(ctx, day)
                    tu = self.timeuntil(times[prayer], 'US/Pacific')
                await ctx.send(
                    '**{}** is **{}** hours and **{}** minutes away.'.format(
                        prayer, tu[0], tu[1]))
        else:
            await ctx.send('I think you misspelled the prayer. Try again.')

    @commands.command(name='setlocation')
    async def setlocation(self, ctx, *, location: str = None):
        if location is None:
            await ctx.send("I don't belive it is possible to live nowhere...")
        else:
            try:
                locations = self.get_location()
                new_location = self.get_lat_long(location.lower()).split(',')
                tz = self.get_timezone(new_location[0], new_location[1])
                locations[ctx.author.id] = [
                    new_location[0], new_location[1],
                    location.capitalize(), tz
                ]
                self.update_location(locations)
                await ctx.send('Set new location to **{}**.'.format(
                    location.capitalize()))
            except:
                await ctx.send(
                    'Oops, I was not able to find **{}**. Try checking your spelling.'
                    .format(location))
                


def setup(bot):
    bot.add_cog(trdCommands(bot))
