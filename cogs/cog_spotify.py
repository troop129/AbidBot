import discord
import pickle
import os
from discord.ext import commands
from discord import Spotify

import base64
import json
import random
import re
import requests
import sys
import urllib

from fuzzysearch import find_near_matches

# Client Keys
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

# Spotify API URLs
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


class SpotifyCommands(commands.Cog, name='Spotify Commands'):
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
  
  def get_token(self):
    client_token = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode('UTF-8')).decode('ascii')
    headers = {"Authorization": "Basic {}".format(client_token)}
    payload = {"grant_type": "client_credentials"}
    token_request = requests.post(SPOTIFY_TOKEN_URL, data=payload, headers=headers)
    access_token = json.loads(token_request.text)["access_token"]
    return access_token

  def request_valid_song(self, access_token, genre=None):

    random_wildcards = ['%25a%25', 'a%25', '%25a',
                        '%25e%25', 'e%25', '%25e',
                        '%25i%25', 'i%25', '%25i',
                        '%25o%25', 'o%25', '%25o',
                        '%25u%25', 'u%25', '%25u']
    wildcard = random.choice(random_wildcards)

    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    song = None
    for i in range(51):
        try:
            song_request = requests.get(
                '{}/search?q={}{}&type=track&offset={}'.format(
                    SPOTIFY_API_URL,
                    wildcard,
                    "%20genre:%22{}%22".format(genre.replace(" ", "%20")),
                    random.randint(0, 200)
                ),
                headers = authorization_header
            )
            song_info = random.choice(json.loads(song_request.text)['tracks']['items'])
            artist = song_info['artists'][0]['name']
            song = song_info['name']
            break
        except IndexError:
            continue
        
    if song is None:
        artist = "Rick Astley"
        song = "Never Gonna Give You Up"

    return [song_info['external_urls']['spotify'], artist, song]

  @commands.command(name = 'randomsong', aliases = ['randomspotify', 'spotifyrandom'])
  async def randomsong(self, ctx, *, genre:str=''):
    args = sys.argv[1:]
    n_args = len(args)
    access_token = self.get_token()
    try:
        with open('storage/genres.json', 'r') as infile:
          valid_genres = json.load(infile)
    except FileNotFoundError:
        await ctx.send("Couldn't find genres file!")
        sys.exit(1)
    if genre == '':
      if n_args == 0:
          selected_genre = random.choice(valid_genres)
      else:
          selected_genre = (" ".join(args)).lower()
    else:
      selected_genre = genre
    
    if selected_genre in valid_genres:
        result = self.request_valid_song(access_token, genre=selected_genre)
        m = await ctx.send('{link}\n**{song}** by **{artist}** in **{genre}**.'.format(link = result[0], artist = result[1], song = result[2], genre = selected_genre.title()))
        await m.add_reaction('a:thumbs_up:812905599242862612')
        await m.add_reaction('a:thumbs_down:812905599103664159')
    else:
        valid_genres_to_text = " ".join(valid_genres)
        try:
            closest_genre = find_near_matches(selected_genre, valid_genres_to_text,  max_l_dist=2)[0].matched
            result = self.request_valid_song(access_token, genre=closest_genre)
            m = await ctx.send('{link}\n**{song}** by **{artist}** in **{genre}**.'.format(link = result[0], artist = result[1], song = result[2], genre = selected_genre.title()))
            await m.add_reaction('a:thumbs_up:812905599242862612')
            await m.add_reaction('a:thumbs_down:812905599103664159')
        except IndexError:
            await ctx.send("Sorry, I couldn't find the genre **{}**.".format(genre))

  @commands.command(name = 'ratesong', aliases = ['rs', 'ratespotify'])
  async def ratesong(self, ctx, m: discord.Member = None):
    isSpotify = False
    if m == None:
      m = ctx.author
    if m.activities:
      for activity in m.activities:
        if isinstance(activity, Spotify):
          f = await ctx.send(f'https://open.spotify.com/track/{activity.track_id}')
          await f.add_reaction('a:thumbs_up:812905599242862612')
          await f.add_reaction('\N{NEUTRAL FACE}')
          await f.add_reaction('a:thumbs_down:812905599103664159')
          isSpotify = True
    if not isSpotify:
      await ctx.send('I don\'t see you listening to Spotify.')
      
  @commands.command(name = 'randomartist', aliases = ['ra'])
  async def randomartist(self, ctx, *, genre:str=''):
    args = sys.argv[1:]
    n_args = len(args)
    access_token = self.get_token()
    try:
        with open('storage/genres.json', 'r') as infile:
          valid_genres = json.load(infile)
    except FileNotFoundError:
        await ctx.send("Couldn't find genres file!")
        sys.exit(1)
    if genre == '':
      if n_args == 0:
          selected_genre = random.choice(valid_genres)
      else:
          selected_genre = (" ".join(args)).lower()
    else:
      selected_genre = genre
    
    if selected_genre in valid_genres:
        result = self.request_valid_song(access_token, genre=selected_genre)
        m = await ctx.send('{link}\n**{song}** by **{artist}** in **{genre}**.'.format(link = result[0], artist = result[1], song = result[2], genre = selected_genre.title()))
        await m.add_reaction('a:thumbs_up:812905599242862612')
        await m.add_reaction('a:thumbs_down:812905599103664159')
    else:
        valid_genres_to_text = " ".join(valid_genres)
        try:
            closest_genre = find_near_matches(selected_genre, valid_genres_to_text,  max_l_dist=2)[0].matched
            result = self.request_valid_song(access_token, genre=closest_genre)
            m = await ctx.send('{link}\n**{song}** by **{artist}** in **{genre}**.'.format(link = result[0], artist = result[1], song = result[2], genre = selected_genre.title()))
            await m.add_reaction('a:thumbs_up:812905599242862612')
            await m.add_reaction('a:thumbs_down:812905599103664159')
        except IndexError:
            await ctx.send("Sorry, I couldn't find the genre **{}**.".format(genre))

def setup(bot):
	bot.add_cog(SpotifyCommands(bot))