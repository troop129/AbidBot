import requests
import json
import random
import asyncio
import discord
import aiohttp
import discord.ext
import typing
import pickle
from discord.ext import commands
import re


class generalCommands(commands.Cog, name='General Server Commands'):
    '''These are the commands for general servers'''
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        infile = open('storage/blacklist', 'rb')
        self.banned = pickle.load(infile)
        infile.close()
        for id in self.banned:
            if int(format(ctx.author.id)) == id:
                return False
        return True

    def getSyn(self, word):
        app_id = 'e762a89e'
        app_key = '47f395f230ba589e1f5874e4a68e27fa'
        language = 'en-us'
        syns = []
        url = 'https://od-api.oxforddictionaries.com/api/v2/entries/' + language + '/' + word.lower(
        )
        r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
        data = json.loads(r.content)
        try:
            for x in data['results'][0]['lexicalEntries'][0]['entries'][0][
                    'senses'][0]['synonyms']:
                syns.append(x['text'])
            return random.choice(syns)
        except:
            return False

    @commands.command(name='inspire', aliases=['ins'])
    async def inspire(self, ctx):
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        await ctx.send(quote)

    @commands.command(name='roast')
    async def roast(self, ctx, member: discord.Member = None):
        response = requests.get(
            "https://evilinsult.com/generate_insult.php?lang=en&type=txt")
        roast = response.text
        roast = roast.replace("&quot;", '"')
        roast = roast.replace("&amp;", '&')
        if int(format(ctx.guild.id)) != 755833429622259913:
            if member != None:
                if self.bot.user.name == member.name:
                    await ctx.send("`ERROR 420: NOT ALLOWED`")
                    await asyncio.sleep(2)
                    await ctx.send(":middle_finger:")
                elif ctx.author.name == member.name:
                    await ctx.send("Roasting yourself eh? I see how it is.")
                    await asyncio.sleep(1)
                    await ctx.send("Well **{}**: {roast}".format(
                        ctx.author.display_name, roast=roast))
                else:
                    await ctx.send('**{}**: {}'.format(member.display_name,
                                                       roast))
            else:
                await ctx.send("Roasting yourself eh? I see how it is.")
                await asyncio.sleep(1)
                await ctx.send("Well **{}**: {roast}".format(
                    ctx.author.display_name, roast=roast))

    @commands.command(name='insult')
    async def insult(self, ctx, member: discord.Member = None):
        if int(format(ctx.guild.id)) != 755833429622259913:
            if member != None:
                if ctx.author.name == member.name:
                    await ctx.send("Insulting yourself? Ok.")
                    await asyncio.sleep(2)
                    response = requests.get(
                        "https://insult.mattbas.org/api/en/insult.txt?who=" +
                        "You")
                    insult = response.text
                    await ctx.send(insult)
                elif self.bot.user.name == member.name:
                    await ctx.send("Hey insult someone else you foofer!")
                else:
                    response = requests.get(
                        "https://insult.mattbas.org/api/en/insult.txt?who=" +
                        member.display_name)
                    insult = response.text
                    await ctx.send('{}.'.format(insult))
            else:
                await ctx.send("Who do I insult, myself?")

    @commands.command(name='compliment')
    async def compliment(self, ctx, member: discord.Member = None):
        if member != None:
            if ctx.author.name == member.name:
                await ctx.send("smh go compliment someone else :rolling_eyes:")
            elif self.bot.user.name == member.name:
                lines = open("./storage/compliments.txt").read().splitlines()
                c = random.choice(lines)
                await ctx.send("Aww thanks! :two_hearts:")
                await asyncio.sleep(2)
                await ctx.send('Heres one for you: ' + c)
            else:
                lines = open("./storage/compliments.txt").read().splitlines()
                c = random.choice(lines)
                await ctx.send("**{}**, {compliment}".format(
                    member.display_name, compliment=c))
        else:
            await ctx.send("I do need someone to compliment you know.")

    @commands.command(name='yomama', aliases=['ym'])
    async def yomama(self, ctx, member: discord.Member = None):
        if int(format(ctx.guild.id)) != 755833429622259913:
            lines = open("./storage/yomama.txt").read().splitlines()
            c = random.choice(lines)
            if member != None:
                if ctx.author.name == member.name:
                    await ctx.send("Your're insulting your own mom?")
                elif self.bot.user.name == member.name:
                    await ctx.send("My mom is off limits, fool.")
                else:
                    await ctx.send("**{}**, {insult}".format(
                        member.display_name, insult=c))
            else:
                await ctx.send("Who's mom do I roast, you doofus? Mine?")

    @commands.command(name='joke')
    async def joke(self, ctx):
        response = requests.get(
            "https://official-joke-api.appspot.com/random_joke")
        payload = response.json()
        await ctx.send(payload['setup'])
        await asyncio.sleep(2)
        await ctx.send(payload['punchline'])

    @commands.command(name='8ball', aliases=['8'])
    async def eightball(self, ctx, *, arg: str = ''):
        if arg != '':
            q = arg
            response = requests.get('https://8ball.delegator.com/magic/JSON/' +
                                    q)
            data = json.loads(response.content)
            question = data['magic']['question']
            answer = data['magic']['answer']
            embed = discord.Embed(
                title="BeedoBot - 8ball",
                description="The answers to all of your questions...")
            embed.set_thumbnail(url="https://i.imgur.com/1WRfu41.png")
            embed.add_field(name="Your Question", value=question, inline=False)
            embed.add_field(name="My Answer", value=answer, inline=False)
            embed.set_footer(text="I hope your query was answered.")
            await ctx.send(embed=embed)
        elif arg == '':
            await ctx.send('I have an 8ball question for you instead...')
            await asyncio.sleep(2)
            await ctx.send('What are you asking me, you troglodyte?')

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

    @commands.command(name='poll')
    async def poll(self, ctx, *, arg=None):
        if arg == None:
            await ctx.send("You need things to poll with...")
        else:
            data = arg
            choices = []
            words = ''
            nums = [
                ':one:', ':two:', ':three:', ':four:', ':five:', ':six:',
                ':seven:', ':eight:', ':nine:'
            ]
            reactions = [
                '<:1:822202649658392627>', '<:2:822202649699942468>',
                '<:3:822202649691815968>', '<:4:822202649649872926>',
                '<:5:822202649633357855>', '<:6:822202648958730240>',
                '<:7:822202649722093598>', '<:8:822202649603473468>',
                '<:9_:822202649650397214>'
            ]
            try:
                if '|' in data:
                    while '|' in data:
                        choices.insert(len(choices), data[:data.index('|')])
                        data = data[data.index('|') + 1:]
                        while data[0] == " ":
                            data = data[1:]
                    choices.insert(len(choices), data)
                    if len(choices) > 9:
                        await ctx.send('You can only have up to 9 options...')
                        return
                    else:
                        count = 0
                        for d in choices:
                            words += '{} = **{}**\n'.format(
                                reactions[count], d)
                            count += 1
                        m = await ctx.send(
                            '**{}** has made a new poll: \n{words}'.format(
                                ctx.author.display_name, words=words))
                        for i in range(0, len(choices)):
                            await m.add_reaction(reactions[i])
                else:
                    await ctx.send('Separate choices with "|" please.')
            except:
                await ctx.send('I think you messed up. Try rephrasing.')

    @commands.command(name='vote')
    async def vote(self, ctx, *, arg=None):
        if arg == None:
            await ctx.send('What do we vote on? Me?')
        else:
            if "?" not in arg:
                arg += "?"
            m = await ctx.send('**{} asks: ** {arg}'.format(
                ctx.author.display_name, arg=arg))
            await m.add_reaction('a:thumbs_up:812905599242862612')
            await m.add_reaction('a:thumbs_down:812905599103664159')

    @commands.command(name='nutella')
    async def nutella(self, ctx):
        options = [
            "<a:nutellaanimate:811831046886522900>",
            "<:Nutella:811683842003697774>",
            "<:WaffleofNutella:812210192028008468>",
            "<:Teehee:812210411377000448>",
            "<:SandwhichofNutella:812210335343706123>",
            "<:NUTELLA:812210524103376956>",
            "<:CrepesofNutella:812210455182311424>",
            "<:CookiesofNutella:812210271678234635>"
        ]
        emoji = random.choice(options)
        await ctx.send(emoji)

    @commands.command(name='countdown')
    async def countdown(self, ctx, *args):
        try:
            arg = args[0]
            letter = arg[-1]
            name = ' - '
            embed = discord.Embed(title="BeedoBot Timer")
            try:
                catcher = args[1]
                for x in args:
                    if args.index(x) != 0:
                        name = name + x + ' '
            except:
                name = ''

            if letter == 's':
                timeleft = int(arg[:-1])
                units = "** seconds left."
            elif letter == 'm':
                timeleft = int(arg[:-1]) * 60
                units = "** minutes left."

            embed.add_field(name="Timer started!" + name,
                            value="You have **" + arg[:-1] + units,
                            inline=False)
            m = await ctx.send(embed=embed)

            while timeleft > 90:
                await asyncio.sleep(60)
                timeleft -= 60
                embed = discord.Embed(title="BeedoBot Timer")
                mins = ''
                if timeleft % 60 == 0:
                    mins = str(int(timeleft / 60))
                    embed.add_field(name="Timer started!" + name,
                                    value="You have **" + mins +
                                    "** minutes left.",
                                    inline=False)
                else:
                    embed.add_field(name="Timer started!" + name,
                                    value="You have **" + str(timeleft / 60) +
                                    "** minutes left.",
                                    inline=False)
                await m.edit(embed=embed)

            while timeleft <= 90 and timeleft > 30:
                await asyncio.sleep(15)
                timeleft -= 15
                embed = discord.Embed(title="BeedoBot Timer")
                embed.add_field(name="Timer started!" + name,
                                value="You have **" + str(timeleft) +
                                "** seconds left.",
                                inline=False)
                await m.edit(embed=embed)

            while timeleft <= 30 and timeleft > 10:
                await asyncio.sleep(5)
                timeleft -= 5
                embed = discord.Embed(title="BeedoBot Timer")
                embed.add_field(name="Timer started!" + name,
                                value="You have **" + str(timeleft) +
                                "** seconds left.",
                                inline=False)
                await m.edit(embed=embed)

            while timeleft <= 10 and timeleft > 1:
                await asyncio.sleep(1)
                timeleft -= 1
                embed = discord.Embed(title="BeedoBot Timer")
                embed.add_field(name="Timer started!" + name,
                                value="You have **" + str(timeleft) +
                                "** seconds left.",
                                inline=False)
                await m.edit(embed=embed)

            if timeleft == 1:
                await asyncio.sleep(1)
                timeleft -= 1
                embed = discord.Embed(title="BeedoBot Timer")
                embed.add_field(name="Timer ended!" + name,
                                value="You have **0** seconds left!",
                                inline=False)
                await m.edit(embed=embed)

        except:
            await ctx.send("Format time correctly please.")
            await asyncio.sleep(2)
            await ctx.send("Fool.")

    @commands.command(name='emojify', aliases=['e', 'emoji'])
    async def emojify(self, ctx, *, arg=None):
        if arg != None:
            converted = ''
            for l in arg:
                if l.isalpha():
                    converted += ':regional_indicator_' + l.lower() + ':' + ' '
                elif l == ' ':
                    converted += '   '
                elif l == '?':
                    converted += ':question: '
                elif l == '!':
                    converted += ':exclamation: '
                else:
                    converted += l + ' '
            await ctx.send(converted)
        else:
            await ctx.send('What do I make into an emoji? You? Ok.')
            await asyncio.sleep(2)
            await ctx.send('<:smallbrain:813895629565984768>')

    @commands.command(name='work', aliases=['study'])
    async def work(self, ctx):
        await ctx.send('https://i.imgur.com/jI6t0cS.png')

    @commands.command(name='sleep')
    async def sleep(self, ctx):
        await ctx.send('https://i.imgur.com/ctzynlC.png')

    @commands.command(name='reverse', aliases=['uno', 'nou', 'no u'])
    async def reverse(self, ctx):
        cards = [
            'https://i.imgur.com/IxDEdxW.png',
            'https://i.imgur.com/3WDcYbV.png'
        ]
        await ctx.send(random.choice(cards))

    @commands.command(name='f', aliases=['rip'])
    async def f(self, ctx):
        cards = [
            'https://tenor.com/view/press-f-pay-respect-coffin-burial-gif-12855021'
        ]
        await ctx.send(random.choice(cards))

    @commands.command(name='avatar', aliases=['a', 'av'])
    async def avatar(self, ctx, member: discord.Member = None):
        author = ''
        choices = [
            'It better not be anime...', "It's an okay pfp...", 'I hate it.',
            'Why not use my face instead?', ':sick:', ':eyes:', ':heart_eyes:',
            ':+1:', 'Need a new one?', "It's time to change...",
            "Almost as pretty as Asma"
        ]
        if member == None:
            author = ctx.author.name
            embed = discord.Embed(title="Your Avatar",
                                  description=random.choice(choices))
            embed.set_image(url=ctx.author.avatar_url)
        elif self.bot.user.name == member.name:
            embed = discord.Embed(
                title="Your Avatar",
                description='LOOK AT THAT BEAUTIFUL FACE OMG!')
            embed.set_image(url=member.avatar_url)
        else:
            author = member.name
            embed = discord.Embed(title="{}'s Avatar".format(author),
                                  description=random.choice(choices))
            embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='servericon', aliases=['si', 'icon'])
    async def servericon(self, ctx):
        choices = [
            'It better not be anime...', "It's an okay icon...", 'I hate it.',
            'Why not use my face instead?', ':sick:', ':eyes:', ':heart_eyes:',
            ':+1:', 'Need a new one?', "It's time to change...",
            "Almost as pretty as Asma..."
        ]
        embed = discord.Embed(title="{}'s Icon".format(ctx.guild.name),
                                  description=random.choice(choices))
        embed.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(name='urban', aliases=['ud'])
    async def urban(self, ctx, *, arg: str = ''):
        if int(format(ctx.guild.id)) != 755833429622259913:
            if arg == '':
                await ctx.send('What are you looking up? Me? Ok.')
                await asyncio.sleep(2)
                await ctx.send(
                    '**BeedoBot**: The #1 best discord bot in the world.')
            else:
                defs = []
                words = []
                arg = arg.lower()
                url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
                querystring = {"term": arg}
                headers = {
                    'x-rapidapi-key':
                    "1097c6051cmsh08616dcf75d9528p131eb8jsn141b3329d1e2",
                    'x-rapidapi-host':
                    "mashape-community-urban-dictionary.p.rapidapi.com"
                }
                response = requests.request("GET",
                                            url,
                                            headers=headers,
                                            params=querystring)
                data = json.loads(response.content)

                try:
                    def1 = data['list'][0]['definition']
                    def1 = def1.replace('[', '')
                    def1 = def1.replace(']', '')
                    defs.append(def1)
                    words.append(data['list'][0]['word'])
                except:
                    pass
                try:
                    def2 = data['list'][1]['definition']
                    def2 = def2.replace('[', '')
                    def2 = def2.replace(']', '')
                    defs.append(def2)
                    words.append(data['list'][1]['word'])
                except:
                    pass
                try:
                    def3 = data['list'][2]['definition']
                    def3 = def3.replace('[', '')
                    def3 = def3.replace(']', '')
                    defs.append(def3)
                    words.append(data['list'][2]['word'])
                except:
                    pass

                embed = discord.Embed(
                    title="Urban Dictionary Definitions",
                    description=
                    "The cool peoples' dictionary. Asked by: **{}**.".format(
                        ctx.author.display_name))
                if arg == 'mushu':
                    embed.add_field(name='Mushu',
                                    value='The best nickname in the world.',
                                    inline=False)
                    embed.add_field(name='Mushu',
                                    value='The dragon from Mulan.',
                                    inline=False)
                    await ctx.send(embed=embed)
                #elif arg == 'abid':
                #embed.add_field(name = 'Abid', value = 'The hottest man in the world.' ,
                #embed.add_field(name = 'Abid', value = 'The hottest man in the world.' , inline=False)
                #await ctx.send(embed=embed)
                elif not words:
                    await ctx.send(
                        'Sorry, I could not find any definitions for that word.'
                    )
                else:
                    count = 0
                    for d in defs:
                        d = (d[:1000] + '..') if len(d) > 1024 else d
                        embed.add_field(name=words[count],
                                        value=d,
                                        inline=False)
                        count += 1

                    await ctx.send(embed=embed)

    @commands.command(name='define', aliases=['dictionary', 'definition'])
    async def define(self, ctx, arg: str = ''):
        if arg == '':
            await ctx.send(
                'Since you failed to give me a word to define, I will get one myself.'
            )
            await asyncio.sleep(2)
            await ctx.send(
                '**{}**: A nincompoop who fails to use a bot properly.'.format(
                    (ctx.author.display_name).capitalize()))
        else:
            app_id = 'e762a89e'
            app_key = '47f395f230ba589e1f5874e4a68e27fa'
            language = 'en-us'
            word_id = arg
            url = 'https://od-api.oxforddictionaries.com/api/v2/entries/' + language + '/' + word_id.lower(
            )
            r = requests.get(url,
                             headers={
                                 'app_id': app_id,
                                 'app_key': app_key
                             })
            if r.status_code == 404:
                await ctx.send(
                    'Oops, **{}** is not a real word. Try checking your spelling.'
                    .format(arg.capitalize()))
            elif r.status_code == 200:
                data = json.loads(r.content)
                embed = discord.Embed(
                    title="Definition of: {}".format(
                        (data['id'].capitalize())),
                    description=
                    "An BeedoBot dictionary call queried by: **{}**.".format(
                        ctx.author.display_name))
                try:
                    embed.add_field(name='Definition',
                                    value=data['results'][0]['lexicalEntries']
                                    [0]['entries'][0]['senses'][0]
                                    ['definitions'][0].capitalize(),
                                    inline=False)
                    try:
                        embed.add_field(
                            name='Example Sentence',
                            value=data['results'][0]['lexicalEntries'][0]
                            ['entries'][0]['senses'][0]['examples'][0]
                            ['text'].capitalize(),
                            inline=False)
                    except:
                        embed.add_field(name='Example Sentence',
                                        value='None given.',
                                        inline=False)
                    await ctx.send(embed=embed)
                except:
                    pass
            else:
                await ctx.send(
                    'The API seems to have failed for some reason. Please try again.'
                )

    @commands.command(name='synonym', aliases=['syn', 'thesaurus'])
    async def synonym(self, ctx, arg: str = ''):
        if arg == '':
            await ctx.send(
                'Since you failed to give me a word to look up, I will get one myself.'
            )
            await asyncio.sleep(2)
            await ctx.send('Synonym of **{}**: **Idiot**'.format(
                (ctx.author.display_name).capitalize()))
        else:
            app_id = 'e762a89e'
            app_key = '47f395f230ba589e1f5874e4a68e27fa'
            language = 'en-us'
            word_id = arg
            url = 'https://od-api.oxforddictionaries.com/api/v2/entries/' + language + '/' + word_id.lower(
            )
            r = requests.get(url,
                             headers={
                                 'app_id': app_id,
                                 'app_key': app_key
                             })
            if r.status_code == 404:
                await ctx.send(
                    'Oops, **{}** is not a real word. Try checking your spelling.'
                    .format(arg.capitalize()))
            elif r.status_code == 200:
                data = json.loads(r.content)
                syns = []
                try:
                    for x in data['results'][0]['lexicalEntries'][0][
                            'entries'][0]['senses'][0]['synonyms']:
                        syns.append(x['text'])
                    await ctx.send(
                        random.choice([
                            f"A synonym for **{arg}** is **{random.choice(syns)}**.",
                            f"Try using **{random.choice(syns)}** instead of **{arg}**."
                        ]))
                except:
                    return await ctx.send(
                        f"I couldn\'t find any synonyms for **{arg}**.")
            else:
                await ctx.send(
                    'The API seems to have failed for some reason. Please try again.'
                )

    @commands.command(name='syns', aliases=['thesaurize', 'mixup'])
    async def syns(self, ctx, *, arg: str = ''):
        if arg == '':
            await ctx.send(
                'Since you failed to give me a sting to look up, I will get one myself.'
            )
            await asyncio.sleep(2)
            await ctx.send('Rewriting **{}**: **A literal idiot**.'.format(
                (ctx.author.display_name).capitalize()))
        else:
            sentence = re.findall(r"[\w']+|[.,!?;:]", arg)
            bsen = ""
            for word in sentence:
                syn = self.getSyn(word)
                if syn != False:
                    bsen += f" {syn}"
                else:
                    if word in {",", ".", "!", "?", ":", ";"}:
                        bsen += word
                    else:
                        bsen += f" {word}"
            await ctx.send(bsen)

    @commands.command(name='meme')
    async def meme(self, ctx):
        try:
            subs = ['dankmemes', 'meme', 'memes']
            comm = random.choice(subs)
            embed = discord.Embed(
                title="BeedoBot Memes",
                description="Shamelessly stolen from r/{}".format(comm))
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                        'https://www.reddit.com/r/{}/new.json?sort=hot'.format(
                            comm)) as r:
                    res = await r.json()
                    embed.set_image(url=res['data']['children'][random.randint(
                        0, 25)]['data']['url'])
                    await ctx.send(embed=embed)
        except:
            await ctx.send('Oops, something went wrong. Please try again!')

    @commands.command(name='reddit')
    async def reddit(self, ctx, arg: str = ''):
        if arg == '':
            await ctx.send('What community do I search?')
        try:
            community = arg.replace('r/', '')
        except:
            pass
        embed = discord.Embed(
            title="BeedoBot Reddit Canvasser",
            description="Shamelessly stolen from r/{}".format(community))
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    'https://www.reddit.com/r/{}/new.json?sort=hot'.format(
                        community)) as r:
                try:
                    res = await r.json()
                    embed.set_image(url=res['data']['children'][random.randint(
                        0, 25)]['data']['url'])
                    await ctx.send(embed=embed)
                except:
                    await ctx.send(
                        'The community you requested is either invalid or not an image-only subreddit.'
                    )

    @commands.command(name='clap')
    async def clap(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send('I guess I will clap to nothing then.')
        else:
            message = arg.replace(' ', ' :clap: ')
            message = ':clap: {} :clap:'.format(message)
            await ctx.send(message)

    @commands.command(name='coinflip', aliases=['hrt', 'headsortails', 'coin'])
    async def coinflip(self, ctx):
        choice = random.randint(1, 3)
        await ctx.send('Flipping a coin...')
        await asyncio.sleep(1.5)
        coin = ''
        if choice == 1:
            coin = 'tails'
        if choice == 2:
            coin = 'heads'
        await ctx.send('I choose **{}**.'.format(coin))

    @commands.command(name='numberchoose',
                      aliases=['randomint', 'randomnumber'])
    async def numberchoose(self, ctx, *, args=None):
        if args is not None:
            nums = args.split(' ')
            if len(nums) <= 1:
                await ctx.send("I can't choose with just one number...")
            else:
                try:
                    least = int(nums[0])
                    most = int(nums[1])
                    if least > most:
                        least, most = most, least
                    elif least == most:
                        await ctx.send("I choose...")
                        await asyncio.sleep(2)
                        await ctx.send(
                            '**{}**! Did you expect something else?'.format(
                                least))
                    else:
                        number = random.randint(least, most)
                        await ctx.send(
                            'Choosing a random number between **{}** and **{}**...'
                            .format(least, most))
                        await asyncio.sleep(2)
                        await ctx.send('I choose **{}**!'.format(number))
                except ValueError:
                    await ctx.send('I cannot choose you do not give numbers...'
                                   )
        else:
            await ctx.send('In order to pick between numbers, I need numbers.')
            await asyncio.sleep(2)
            await ctx.send('*GiMmIe ThE nUmBeRs MaN!*')

    @commands.command(name='echo')
    async def echo(self,
                   ctx,
                   channel: typing.Optional[discord.TextChannel] = None,
                   *,
                   args=None):
        if args is None:
            await ctx.send('What do I echo?')
        else:
            if channel is None:
                await ctx.send(args)
            else:
                await channel.send(args)

    @commands.command(name='search', aliases=['bing', 'google'])
    async def search(self, ctx, *, args=None):
        if args is None:
            await ctx.send('What do I look up?')
        else:
            url = "https://bing-web-search1.p.rapidapi.com/search"
            querystring = {
                "q": args,
                "mkt": "en-us",
                "textFormat": "Raw",
                "safeSearch": "Off",
                "freshness": "Day"
            }
            headers = {
                'x-bingapis-sdk': "true",
                'x-rapidapi-key':
                "1097c6051cmsh08616dcf75d9528p131eb8jsn141b3329d1e2",
                'x-rapidapi-host': "bing-web-search1.p.rapidapi.com"
            }
            response = requests.request("GET",
                                        url,
                                        headers=headers,
                                        params=querystring)
            data = json.loads(response.content)

            try:
                url = data['webPages']['webSearchUrl']  #search url
                matches = data['webPages'][
                    'totalEstimatedMatches']  # number of matches
                embed = discord.Embed(
                    title="Bing results for: {}".format((args.capitalize())),
                    description="I found **{}** matches.".format(matches),
                    url=url)

                for x in range(0, 4):
                    link = data['webPages']['value'][x]['url']
                    urltitle = data['webPages']['value'][x]['name']
                    snippet = data['webPages']['value'][x]['snippet']
                    embed.add_field(name='{}: {}'.format(x + 1, urltitle),
                                    value='{} [Link]({})'.format(
                                        snippet, link),
                                    inline=False)

                await ctx.send(embed=embed)
            except:
                await ctx.send(
                    'Oops, I could not find any results for that word :/')

    @commands.command(name='wonky',
                      aliases=['sarcastic', 'caps', 'sarcasm', 's'])
    async def wonky(self, ctx, *, args=None):
        if args == None:
            await ctx.send('I gUeSs IlL mAkE fUn Of YoU iNsTeAd...')
        else:
            ret = ""
            i = True
            for char in args:
                if i:
                    ret += char.upper()
                else:
                    ret += char.lower()
                if char != ' ':
                    i = not i
            await ctx.send(ret)

    @commands.command(name='translate', aliases=['googletranslate', 'trans'])
    async def translate(self, ctx, *args):
        if len(args) < 3:
            return await ctx.send(
                'Format your query like this example: `!translate en es "hello world"`'
            )
        source = args[0]
        target = args[1]
        if len(args) > 3:
            query = " ".join(args[2:]).encode('utf-8')
        else:
            query = args[2].encode('utf-8')
        if source == '~' or source == 'detect':
            payload = "q={}&format=text&target={}".format(query, target)
        else:
            payload = "q={}&format=text&target={}&source={}".format(
                query, target, source)
        url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'accept-encoding': "application/gzip",
            'x-rapidapi-key':
            "4df2bafccbmsh2817faa7ff48e95p11abd2jsnd77c485a3312",
            'x-rapidapi-host': "google-translate1.p.rapidapi.com"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        data = json.loads(response.content)
        #try:
        if 1 == 1:
            if source != '~' or source != 'detect':
                await ctx.send(data)
                #await ctx.send(data['data']['translations'][0]['translatedText'])
            else:
                translation = data['data']['translations'][0]['translatedText']
                lang = data['data']['translations'][0][
                    'detectedSourceLanguage']
                await ctx.send(
                    "I detected **{}**, and translated it into this:\n{}".
                    format(lang, translation))
        #except:
        else:
            await ctx.send(
                "I don't think you formatted your languages right. Please try again.\nFor a list of ISO 639-1 codes, check out this link: <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>"
            )

    @commands.command(name='github', aliases=['git', 'source'])
    async def github(self, ctx):
        await ctx.send(
            'Check out my source code: https://github.com/troop129/BeedoBot')

    @commands.command(name='gif', aliases=['giphy'])
    async def gif(self, ctx, *, q: str = ''):
        if q == '':
            url = "https://api.giphy.com/v1/gifs/random"
            querystring = {"api_key": "FfXibyqNj1KFcDa6g6aZnqDbmWsYrn9Q"}
            response = requests.request("GET", url, params=querystring)
            data = json.loads((response.content))
            gif = data['data']['url']
        else:
            try:
                url = "https://api.giphy.com/v1/gifs/search"
                querystring = {
                    "api_key": "FfXibyqNj1KFcDa6g6aZnqDbmWsYrn9Q",
                    "q": q
                }
                response = requests.request("GET", url, params=querystring)
                data = json.loads((response.content))
                gifs = []
                for i in data['data']:
                    gifs.append(i['url'])
                gif = random.choice(gifs)
            except:
                return await ctx.send(
                    'I couldn\'t find any GIFs for **{}**.'.format(q))
        await ctx.send(gif)


def setup(bot):
    bot.add_cog(generalCommands(bot))
