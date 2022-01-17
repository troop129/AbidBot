import re
import random
import asyncio
import discord
import discord.ext
import pickle
from discord.ext import commands

class TicTacToe(commands.Cog, name='Tic Tac Toe Commands'):
    """Pretty self-explanatory"""

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

    boards = {}

    def create(self, server_id, player1, player2):
        self.boards[server_id] = Board(player1, player2)
        return self.boards[server_id].challengers["x"]

    @commands.group(aliases=["tic", "tac", "toe", "ttt"], invoke_without_command=True)
    @commands.guild_only()
    async def tictactoe(self, ctx, *, option: str = ''):
        player = ctx.message.author
        board = self.boards.get(ctx.message.guild.id)

        if not board:
            await ctx.send("There are currently no TicTacToe games setup! Use !challenge <mention> to start one.")
            return
        if not board.can_play(player):
            await ctx.send("You cannot play right now!")
            return
        if option == '':
          await ctx.send("Where do I place it? On you?")
          return
        
        top = re.search("top", option)
        middle = re.search("middle", option)
        bottom = re.search("bottom", option)
        left = re.search("left", option)
        right = re.search("right", option)

        if top and bottom:
            await ctx.send("That is not a valid location! Use some logic, come on!")
            return
        if left and right:
            await ctx.send("That is not a valid location! Use some logic, come on!")
            return
        
        if not top and not bottom and not left and not right and not middle:
            await ctx.send("Please provide a valid location to play!")
            return

        x = 0
        y = 0
        
        if top:
            x = 0
        if bottom:
            x = 2
        if left:
            y = 0
        if right:
            y = 2
        
        if middle and not (top or bottom or left or right):
            x = 1
            y = 1
        if (top or bottom) and not (left or right):
            y = 1
        elif (left or right) and not (top or bottom):
            x = 1
        if not board.update(x, y):
            await ctx.send("Someone has already played there!")
            return
        
        winner = board.check()
        if winner:
            loser = (
                board.challengers["x"]
                if board.challengers["x"] != winner
                else board.challengers["o"]
            )
            await ctx.send(
                "**{}** has won this game of TicTacToe! Better luck next time **{}**.".format(
                    winner.display_name, loser.display_name
                )
            )
            try:
                del self.boards[ctx.message.guild.id]
            except KeyError:
                pass
        else:
            if board.full():
                await ctx.send("This game has ended in a tie!")
                try:
                    del self.boards[ctx.message.guild.id]
                except KeyError:
                    pass
            else:
                player_turn = (
                    board.challengers.get("x")
                    if board.X_turn
                    else board.challengers.get("o")
                )
                fmt = str(board) + "\n**{}**: It is now your turn to play!".format(
                    player_turn.display_name
                ) 
                await ctx.send(fmt)

    @commands.command(name="start", aliases=["challenge", "create", "tttstart"])
    @commands.guild_only()
    async def start_game(self, ctx, player2: discord.Member=None):
        player1 = ctx.message.author
        if self.boards.get(ctx.message.guild.id) is not None:
            await ctx.send(
                "Sorry, only one Tic-Tac-Toe game can be running per server!"
            )
            return
        if player2 == ctx.message.guild.me:
            await ctx.send(
                "You want to play? Alright lets play."
            )
            await asyncio.sleep(.5)
            await ctx.send("I win, so quick you didn't even notice it.")
            return
        if player2 == player1:
            await ctx.send(
                "You can't play yourself, I won't allow it. Go find some friends."
            )
            await asyncio.sleep(2)
            await ctx.send(
                "Unless you dont have any... :skull:"
            )
            return
        if player2 == None:
            await ctx.send(
                "Who are you playing with? Me? I wont allow it."
            )
            return

        x_player = self.create(ctx.message.guild.id, player1, player2)
        fmt = "A tictactoe game has just started between **{}** and **{}**!\n".format(
            player1.display_name, player2.display_name
        )
        fmt += str(self.boards[ctx.message.guild.id])
        fmt += (
            "I have decided at random that **{}** is going to play **X** this game, and thus will go first! "
            "Use the `{}tictactoe` command, and a position, to choose where you want to play. Use `!ttt help` for help.".format(
                x_player.display_name, ctx.prefix
            )
        )
        await ctx.send(fmt)

    @tictactoe.command(name="delete", aliases=["stop", "remove", "end"])
    @commands.guild_only()
    async def stop_game(self, ctx):
        if self.boards.get(ctx.message.guild.id) is None:
            await ctx.send("There are no tictactoe games running on this server!")
            return

        del self.boards[ctx.message.guild.id]
        await ctx.send(
            "I have just stopped the game of TicTacToe, a new one should be able to be started now!"
        )

    #@tictactoe.command(name="help")
    #@commands.guild_only()
    #async def stop_game(self, ctx):



class Board:
    def __init__(self, player1, player2):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        if random.SystemRandom().randint(0, 1):
            self.challengers = {"x": player1, "o": player2}
        else:
            self.challengers = {"x": player2, "o": player1}
        self.X_turn = True

    def full(self):
        for row in self.board:
            if " " in row:
                return False  
        return True

    def can_play(self, player):
        if self.X_turn:
            return player == self.challengers["x"]
        else:
            return player == self.challengers["o"]

    def update(self, x, y):
        letter = "x" if self.X_turn else "o"
        if self.board[x][y] == " ":
            self.board[x][y] = letter
        else:
            return False
        self.X_turn = not self.X_turn
        return True

    def check(self):
        if (
            self.board[0][0] == self.board[0][1]
            and self.board[0][0] == self.board[0][2]
            and self.board[0][0] != " "
        ):
            return self.challengers[self.board[0][0]]
        if (
            self.board[0][0] == self.board[1][0]
            and self.board[0][0] == self.board[2][0]
            and self.board[0][0] != " "
        ):
            return self.challengers[self.board[0][0]]
        if (
            self.board[0][0] == self.board[1][1]
            and self.board[0][0] == self.board[2][2]
            and self.board[0][0] != " "
        ):
            return self.challengers[self.board[0][0]]

        if (
            self.board[0][2] == self.board[1][2]
            and self.board[0][2] == self.board[2][2]
            and self.board[0][2] != " "
        ):
            return self.challengers[self.board[0][2]]
        if (
            self.board[0][2] == self.board[1][1]
            and self.board[0][2] == self.board[2][0]
            and self.board[0][2] != " "
        ):
            return self.challengers[self.board[0][2]]

        if (
            self.board[2][2] == self.board[2][1]
            and self.board[2][2] == self.board[2][0]
            and self.board[2][2] != " "
        ):
            return self.challengers[self.board[2][2]]

        if (
            self.board[1][1] == self.board[0][1]
            and self.board[1][1] == self.board[2][1]
            and self.board[1][1] != " "
        ):
            return self.challengers[self.board[1][1]]

        if (
            self.board[1][1] == self.board[1][0]
            and self.board[1][1] == self.board[1][2]
            and self.board[1][1] != " "
        ):
            return self.challengers[self.board[1][1]]

        return None

    def __str__(self):
        _board = " {}  |  {}  |  {}\n".format(
            self.board[0][0], self.board[0][1], self.board[0][2]
        )
        _board += "———————————————\n"
        _board += " {}  |  {}  |  {}\n".format(
            self.board[1][0], self.board[1][1], self.board[1][2]
        )
        _board += "———————————————\n"
        _board += " {}  |  {}  |  {}\n".format(
            self.board[2][0], self.board[2][1], self.board[2][2]
        )
        return "```\n{}```".format(_board)


def setup(bot):
    bot.add_cog(TicTacToe(bot))