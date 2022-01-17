import discord
import pickle
import os
from discord.ext import commands
from discord import Spotify

from collections.abc import Sequence

# Client Keys
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

# Spotify API URLs
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


class SpotifyUtilityCommands(commands.Cog, name='Spotify Commands'):
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

    def make_sequence(self, seq):
        if seq is None:
            return ()
        if isinstance(seq, Sequence) and not isinstance(seq, str):
            return seq
        else:
            return (seq, )

    def reaction_check(self, message=None, emoji=None, author=None, ignore_bot=True):
        message = self.make_sequence(message)
        message = tuple(m.id for m in message)
        emoji = self.make_sequence(emoji)
        author = self.make_sequence(author)

        def check(reaction, user):
            if ignore_bot and user.bot:
                return False
            if message and reaction.message.id not in message:
                return False
            if emoji and reaction.emoji not in emoji:
                return False
            if author and user not in author:
                return False
            return True

        return check


def setup(bot):
    bot.add_cog(SpotifyUtilityCommands(bot))
