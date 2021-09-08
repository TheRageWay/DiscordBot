#Discord Bot for DKP System

#test server id = 877528142909161572

#Token
def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

#Imports
import asyncio
from sqlite3.dbapi2 import Cursor
from typing_extensions import Concatenate
import discord
import logging
from discord.ext import commands
import sqlite3

#Variables
intents = discord.Intents(messages=True, guilds=True)
intents.members = True
intents.reactions = True
intents.typing = True
intents.presences = True
bot = commands.Bot(command_prefix='$', case_insensitive=True, intents=intents)
token = read_token()
logger = logging.getLogger('discord')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


#Debug Logging
logger.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler) 

#Ping Command
@bot.command()
async def ping(ctx):

        id = bot.get_guild(877528142909161572)
        channels = ['dkp']

        if str(ctx.channel) in channels:
                await ctx.channel.send('pong!')

#Help Command
@bot.command()
async def helpme(ctx):

        id = bot.get_guild(877528142909161572)
        channels = ['dkp']

        if str(ctx.channel) in channels:

                embed = discord.Embed(title='**List of commands**', colour=discord.Colour(0x0ECA14), description='Some useful commands')
                embed.set_image(url='https://cdn.discordapp.com/icons/184864850059460609/293ef38d13267880ba274086a16e7593.png?size=128')
                embed.set_thumbnail(url='https://cdn.discordapp.com/icons/184864850059460609/293ef38d13267880ba274086a16e7593.png?size=32')
                embed.set_author(name='Warband', url='https://discordapp.com', icon_url='')
                embed.set_footer(text='Hope this Helps!')
                embed.add_field(name='$hello', value='Greets the user')
                embed.add_field(name='$users', value='Shows how many users are in the server')
                embed.add_field(name='$ping', value='ping the bot to see if it is online')
                embed.add_field(name='$AddPoints', value='Adds points to the user (WiP)')
                embed.add_field(name='$ShowPoints', value='Shows users how many points they have (WiP)')
                embed.add_field(name='$RemovePoints', value='Removes points from the user (WiP)')
                await ctx.channel.send(content=None, embed=embed)

#Users Command
@bot.command()
async def users(ctx):

        id = bot.get_guild(877528142909161572)
        channels = ['dkp']

        if str(ctx.channel) in channels:
                await ctx.channel.send(f'# of Users: {id.member_count}')

#Hello Command
@bot.command()
async def hello(ctx):

        id = bot.get_guild(877528142909161572)
        channels = ['dkp']

        if str(ctx.channel) in channels:
                await ctx.channel.send("Hi")

#Add Points Command
@bot.command()
async def addpoints(ctx, arg1, arg2):
        id = bot.get_guild(877528142909161572)
        arg1 = int(arg1)
        channels = ['dkp']
        #print(ctx.message.author.id)
 
        if ctx.message.author.guild_permissions.send_messages:
                if str(ctx.channel) in channels:
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select Points FROM Test WHERE User_ID = {ctx.message.author.id}")
                        result = cursor.fetchone()
                        points = result[0]
                        secondUser = arg2.mention
                        print(secondUser)
                        if result is None:
                                sql1 = ("INSERT INTO Test(Guild_iD, Points, User_ID) VALUES(?,?,?)")
                                val1 = (ctx.guild.id,0,ctx.message.author.id)
                        #cursor.execute(sql1,val1)
                        if isinstance(arg1,int) == False:
                                await ctx.channel.send(f'{arg1} is an invalid number')     
                        else:
                                sql = ("UPDATE Test SET Points = ? WHERE User_ID = ?")
                                val = (arg1 + points,ctx.message.author.id) 
                                await ctx.channel.send(f'{ctx.message.author} Has {arg1+points} available points') 
                        cursor.execute(sql,val) 
                        db.commit()
                        cursor.close()
                        db.close()

#Add Points Command
@bot.command()
async def removepoints(ctx, arg1, arg2):
        id = bot.get_guild(877528142909161572)
        arg1 = int(arg1)
        channels = ['dkp']
        #print(ctx.message.author.id)
 
        if ctx.message.author.guild_permissions.send_messages:
                if str(ctx.channel) in channels:
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select Points FROM Test WHERE User_ID = {ctx.message.author.id}")
                        result = cursor.fetchone()
                        points = result[0]
                        secondUser = arg2.mention
                        check = points - arg1
                        if result is None:
                                await ctx.channel.send(f'That user has no points.')
                        #cursor.execute(sql1,val1)
                        if isinstance(arg1,int) == False & check > 0:
                                await ctx.channel.send(f'{arg1} is an invalid number')     
                        else:
                                sql = ("UPDATE Test SET Points = ? WHERE User_ID = ?")
                                val = (points - arg1,ctx.message.author.id) 
                                await ctx.channel.send(f'{ctx.message.author} Has {arg1+points} available points.') 
                        cursor.execute(sql,val) 
                        db.commit()
                        cursor.close()
                        db.close()
                               
#on_connect
@bot.event
async def on_connect():
        print('DKP bot is now connected to discord!')

#on_ready
@bot.event
async def on_ready():
        db = sqlite3.connect('Test.sqlite')
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Test(
                guild_id Text,
                points Int,
                user_ID Int
                )
                ''')
        print('DKP system is running')
  

#on_disconnect
@bot.event
async def on_disconnect():
        print('DKP bot has disconnected from discord')

#on_member_join
@bot.event
async def on_member_join(member):
        for channel in member.guild.channels:
                if str(channel) == 'welcome':
                        await channel.send(f'Welcome to the Warband {member.mention} To get started using the DKP system, please use the #dkp channel and use the $helpme command.')

bot.run(token)