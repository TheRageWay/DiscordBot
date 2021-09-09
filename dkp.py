#Discord Bot for DKP System

#test server id = 877528142909161572

#Token
def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

#Imports
import asyncio
from asyncio.events import TimerHandle
from asyncio.windows_events import NULL
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
                embed.add_field(name='$AddPoints <Amount> <UsersName>', value='Adds points to the user ')
                embed.add_field(name='$ShowPoints <UsersName>', value='Shows users how many points they have ')
                embed.add_field(name='$RemovePoints <Amount> <UsersName>', value='Removes points from the user ')
                embed.add_field(name='$RemoveAllPoints <UsersName>', value='Removes all points from the user ')
                embed.add_field(name='$UserPoints <UsersName>', value='Points for the specified user ')
                embed.add_field(name='$AddItem <Item Name> <Item Cost>', value='Adds an item to the store')
                embed.add_field(name='$BuyItem <ItemName>', value='Buy an Item from the store')
                embed.add_field(name='$ItemCost <ItemName>', value='Total cost for an item')
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
async def addpoints(ctx, arg1, user: discord.Member):
        id = bot.get_guild(877528142909161572)
        channels = ['dkp']
        #print(ctx.message.author.id)
        #print(format(user.id))
        if ctx.message.author.guild_permissions.send_messages:
                if str(ctx.channel) in channels:
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select Points FROM Test WHERE User_ID = {user.id}")
                        result = cursor.fetchone()
                        print(result)
                        if result == None:
                                sql1 = ("INSERT INTO Test(Guild_iD, Points, User_ID) VALUES(?,?,?)")
                                val1 = (ctx.guild.id,0,user.id)
                                cursor.execute(sql1,val1)
                                db.commit()
                                cursor.close()
                                db.close()
                                db = sqlite3.connect('Test.sqlite')
                                cursor = db.cursor()
                                cursor.execute(f"Select Points FROM Test WHERE User_ID = {user.id}")
                                result = cursor.fetchone()
                                print('Added')
                        if int(arg1) != int:
                                arg1 = int(arg1)
                                points = result[0]
                                sql = ("UPDATE Test SET Points = ? WHERE User_ID = ?")
                                val = (arg1 + points,user.id) 
                                await ctx.channel.send(f'{user.name} Has {arg1+points} points available.') 
                                cursor.execute(sql,val) 
                                db.commit()
                                cursor.close()
                                db.close()     
                        else:
                                await ctx.channel.send(f'{arg1} is an invalid number.') 
                                

#Remove Points Command
@bot.command()
async def removepoints(ctx, arg1: str, user: discord.Member):
        id = bot.get_guild(877528142909161572)
        channels = ['dkp']
 
        if ctx.message.author.guild_permissions.send_messages:
                if str(ctx.channel) in channels:
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select Points FROM Test WHERE User_ID = {user.id}")
                        result = cursor.fetchone()
                        points = result[0]
                        arg1 = int(arg1)
                        check = points - arg1
                        if result is not None:
                                print(user.id)
                                print(ctx.message.author.id)
                                sql = ("UPDATE Test SET Points = ? WHERE User_ID = ?")
                                val = (check,user.id) 
                                await ctx.channel.send(f'{user.name} Has {check} available points.') 
                                cursor.execute(sql,val) 
                                db.commit()
                                cursor.close()
                                db.close()      
                        else:
                                await ctx.channel.send(f'That user has no points.')
                        

#Remove Points Command
@bot.command()
async def removeallpoints(ctx, user: discord.Member):
        id = bot.get_guild(877528142909161572)
        channels = ['dkp']
 
        if ctx.message.author.guild_permissions.send_messages:
                if str(ctx.channel) in channels:
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select Points FROM Test WHERE User_ID = {user.id}")
                        result = cursor.fetchone()
                        points = result[0]
                        check = points - points
                        if result is not None:
                                sql = ("UPDATE Test SET Points = ? WHERE User_ID = ?")
                                val = (check,ctx.message.author.id) 
                                await ctx.channel.send(f'{user.name} Has {check} available points.') 
                                cursor.execute(sql,val) 
                                db.commit()
                                cursor.close()
                                db.close()
                        else:
                                await ctx.channel.send(f'That user has no points.')

                        

#Points Command
@bot.command()
async def Showpoints(ctx, user: discord.Member):
        id = bot.get_guild(877528142909161572)
        channels = ['dkp']
 
        if ctx.message.author.guild_permissions.send_messages:
                if str(ctx.channel) in channels:
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select Points FROM Test WHERE User_ID = {ctx.message.author.id}")
                        result = cursor.fetchone()
                        points = result[0]
                        await ctx.channel.send(f'{user.name} has {points} Points.')
                        db.commit()
                        cursor.close()
                        db.close()
                

#AddItems Command
@bot.command()
async def AddItem(ctx, item ,cost):
        id = bot.get_guild(877528142909161572)
        channels = ['dkp']
 
        if ctx.message.author.guild_permissions.send_messages:
                if str(ctx.channel) in channels:
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select cost FROM Items WHERE ItemName = '{item}'")
                        result = cursor.fetchone()
                        print(result)
                        if result is not None: 
                                await ctx.channel.send(f'That Item Exists.')
                        elif result is None:
                                sql = ("INSERT INTO Items(Guild_iD,Cost,ItemName) VALUES(?,?,?)")
                                val = (ctx.guild.id,cost,item)  
                                cursor.execute(sql,val) 
                                db.commit()
                                cursor.close()
                                db.close()
                                await ctx.channel.send(f'{item} Has been added for {cost} points.')

#AddItems Command
@bot.command()
async def BuyItem(ctx, item):
        id = bot.get_guild(877528142909161572)
        channels = ['dkp']
 
        if ctx.message.author.guild_permissions.send_messages:
                if str(ctx.channel) in channels:
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select cost FROM Items WHERE ItemName = '{item}'")
                        price = cursor.fetchone()
                        cursor.execute(f"Select Points FROM Test WHERE User_ID = {ctx.message.author.id}")
                        points = cursor.fetchone()
                        print(price[0])
                        print(points[0])
                        balance = points[0] - price[0]
                        if price is None:
                                await ctx.channel.send(f'{item} Has Not Been Added To The Store.')
                        elif points is None:
                                await ctx.channel.send(f'You do not have any points')
                        elif balance < 0:
                                await ctx.channel.send(f'You do not have enough points purchase this item.')
                        elif balance >= 0:
                                sql = ("UPDATE Test SET Points = ? WHERE User_ID = ?")
                                val = (balance,ctx.message.author.id) 
                                cursor.execute(sql,val) 
                                db.commit()
                                cursor.close()
                                db.close()
                                await ctx.channel.send(f'{ctx.message.author.name} has purchased {item} and has {balance} remaining points left.') 
#ItemCost Command
@bot.command()
async def ItemCost(ctx, item):
        id = bot.get_guild(877528142909161572)
        channels = ['dkp']
 
        if ctx.message.author.guild_permissions.send_messages:
                if str(ctx.channel) in channels:
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select cost FROM Items WHERE ItemName = '{item}'")
                        result = cursor.fetchone()
                        if result is not None:
                                await ctx.channel.send(f'The {item} costs {result[0]} points.')
                        else: 
                                await ctx.channel.send(f'That Item Does Not Exists.')

#UserPoints Command
@bot.command()
async def userpoints(ctx, user: discord.Member):
        id = bot.get_guild(877528142909161572)
        channels = ['dkp']
 
        if ctx.message.author.guild_permissions.send_messages:
                if str(ctx.channel) in channels:
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select Points FROM Test WHERE User_ID = {user.id}")
                        result = cursor.fetchone()
                        points = result[0]
                        await ctx.channel.send(f'{user.name} has {points} Points.')
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
        db.commit()
        cursor.close()
        db.close()
        db = sqlite3.connect('Test.sqlite')
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Items(
                guild_id Text,
                Cost Int,
                ItemName Text
                )
                ''')
        db.commit()
        cursor.close()
        db.close()
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