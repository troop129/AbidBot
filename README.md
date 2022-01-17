# AbidBot (Beta)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

AbidBot is a private discord bot and pet project of the developer, Abid. The majority of his code is available for free in this repository, feel free to take what you wish and integrate it into your own projects.

## About AbidBot's Code
AbidBot is written fully in Python, using [discord.py](https://github.com/Rapptz/discord.py) by [Rapptz](https://github.com/Rapptz/). AbidBot makes use of cogs to organize the code. A lot of the commands were in the "general" cog, and I decided to get organized but was too lazy to move them around, so about half are in [cogs.cog_general](https://github.com/troop129/AbidBot/blob/main/cogs/cog_general.py) and the rest are distributed among other files, based on what type of command it is. 

The majority of the code is from my own brain but some were definitely taken from random StackOverflow posts, and I wish I could remember and link it. Sorry for stealing your code.

## Can I run AbidBot on my own server?
No, you probably can't in the form it is in this repo. This is merely an exhibition of some of my favorite snippets of code. You are welcome to take what you like and use it for your own bots, but I did not write AbidBot with portability in mind. Sorry.

## Favorite Commands

Now that the boring parts are out the way, we can get to the fun parts. Below are examples of some of my favorite commands, with the code that makes it run.

### !choose *{iterations} {option1}|{option2}|...|{optionx}
When you can't make up your mind, make AbidBot do it.

![choose demo](https://i.imgur.com/hcXRyM6.gif)

This was quite a challenging and fun command to write, since I had to take in account the optional variable in the beginning which would determining how many times to run the choose, and to print that as many times as needed. The full code is below:
```python
@commands.command(name='choose')
async def choose(self, ctx, *, arg=None):
    if arg == None:
        await ctx.send("What do I choose between, you foofer?")
    else:
        data = arg
        try:
            if '|' in data:
                if '*' in data:
                    t = int("".join(filter(str.isdigit, data.split('*')[1][0:3].strip())))
                    data = " ".join(data.split('*')[1].split(' ')[1:])
                    await ctx.send(f"Choosing **{t}** times...")
                else:
                    t = 1
                    await ctx.send("Choosing...")
                await asyncio.sleep(2)
                await ctx.send(" \n".join(
                    map(str, [
                        random.choice([a.strip() for a in data.split('|')])
                        for a in range(0, t)
                    ])))
            else:
                await ctx.send('Separate choices with "|" please.')
        except:
            await ctx.send('I think you messed up. Try rephrasing.')
```
The `int("".join(filter(str.isdigit, data.split('*')[1][0:3].strip())))` extracts the number of iterations, if needed, and the line below takes out that data, in order to split and print. That was quite interesting to come up with. Although I may have found it on Stack, I'm not sure.

### !fr {flight #}

For when you are trying to track a friend in the sky.

![fr demo](https://i.imgur.com/rJpxd05.gif)

I thought flightradar24 would have an API, but I couldn't find one when I made this command. Luckily someone had written an unofficial API in python, called [FlightRadarAPI](https://github.com/JeanExtreme002/FlightRadarAPI). Thanks to you random man. It did spit out a butt-ton of data, so I had to sort through it all which was quite fun. In the end, we got this:
```python
@commands.group(name = 'flightradar', aliases = ['fr', 'flights'], invoke_without_command = True)
  async def flightradar(self, ctx, id:str=''):
    if id == '':
      embed = discord.Embed(title="BeedoBot x FlightRadar24", colour=discord.Colour(0x1), description='Query the reams of data on flightradar24.com. Start all commands with "!flightradar".')
      embed.add_field(name="image", value="`!fr image <flight number>`", inline=True)
      await ctx.send(embed=embed)
    else:
      fr = flightradar24.Api()
      data = fr.get_flight(id)
      flight = self.liveFlightFinder(data)
      image = data['result']['response']['aircraftImages'][0]['images']['large'][1]['src']
      airline = flight['airline']['name']
      destination = flight['airport']['destination']['name']
      dcode = flight['airport']['destination']['code']['iata']
      origin = flight['airport']['origin']['name']
      ocode = flight['airport']['origin']['code']['iata']
      departure = self.convertUnix(flight['time']['real']['departure'])
      arrival = self.convertUnix(flight['time']['estimated']['arrival'])

      embed = discord.Embed(title="BeedoBot x FlightRadar24", colour=discord.Colour(0x1), description='Data on flight {}.'.format(id))
      embed.set_thumbnail(url = image)
      embed.add_field(name="Airline".format(airline), value="{}".format(airline), inline=False)
      embed.add_field(name="Origin", value="{} ({})".format(origin, ocode), inline=False)
      embed.add_field(name="Destination", value="{} ({})".format(destination, dcode), inline=False)
      embed.add_field(name="Departure", value="{}".format(departure),inline=False)
      embed.add_field(name="Arrival", value="{}".format(arrival),inline=False)
      await ctx.send(embed=embed)
```
Not very interesting code, but it was quite annoying to write so here's the credit it gets.

### !prayertime *{prayer}

For all my Muslim brothers and sisters, AbidBot can tell you what time the prayers are, either all at once or just one specific prayer. If you don't set a location, it gives the default Roseville one.

![pt demo](https://i.imgur.com/faeDPNs.gif)

(Excuse the MSABot demo, AbidBot command broke.)

This command involved helper commands upon helper commands. It's kind of insane how complex it is. It has to make a request based on text location to a coordinates API, then to a timezone API, then to prayertime API, then process all the data with datetime. Quite fun. This is the main command:

```python
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
```

As you can see, it also makes use of pickle to store locations so you don't have to keep reminding it.

This is the aforementioned **!setlocation**:
```python
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
```
This stores the data in the pickle, both timezone and the text so I can call it back when serving the embed, like "prayer time in Dallas".
