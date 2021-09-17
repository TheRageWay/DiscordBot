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
import logging.handlers
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
Logger = logging.getLogger('discord')
handler = logging.FileHandler(filename='discord.log', encoding=None, mode='w')
logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
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
                embed.add_field(name='$AddPoints <Amount> <UsersName> <"Reason">', value='Adds points to the user ')
                embed.add_field(name='$ShowPoints <UsersName>', value='Shows users how many points they have ')
                embed.add_field(name='$RemovePoints <Amount> <UsersName>', value='Allows admins to remove points from the user ')
                embed.add_field(name='$RemoveAllPoints <UsersName>', value='Allows admins to remove all points from the user ')
                embed.add_field(name='$UserPoints <UsersName>', value='Points for the specified user ')
                embed.add_field(name='$AddItem <Item Name> <Item Cost>', value='Adds an item to the store')
                embed.add_field(name='$BuyItem <ItemName>', value='Buy an Item from the store')
                embed.add_field(name='$ItemCost <ItemName>', value='Total cost for an item')
                embed.add_field(name='$Store', value='Displayes the items within the store.')
                embed.add_field(name='$MyInventory', value='Displays the items within your inventory')
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
async def addpoints(ctx, arg1, user: discord.Member,Disc):
        id = bot.get_guild(877528142909161572)
        channels = ['dkp']
        #print(ctx.message.author.id)
        #print(format(user.id))
        if str(ctx.channel) in channels:
                db = sqlite3.connect('Test.sqlite')
                cursor = db.cursor()
                cursor.execute(f"Select Points FROM Points WHERE User_ID = {user.id}")
                result = cursor.fetchone()
                print(result)
                if result is None:
                        sql1 = ("INSERT INTO Points(Guild_iD, Points, User_ID) VALUES(?,?,?)")
                        val1 = (ctx.guild.id,0,user.id)
                        cursor.execute(sql1,val1)
                        db.commit()
                        cursor.close()
                        db.close()
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select Points FROM Points WHERE User_ID = {user.id}")
                        result = cursor.fetchone()
                        print('Added')
                if int(arg1) != int:
                        arg1 = int(arg1)
                        points = result[0]
                        if arg1 < 100001:
                                sql = ("UPDATE Points SET Points = ? WHERE User_ID = ?")
                                val = (arg1 + points,user.id) 
                                await ctx.channel.send(f'{user.name} Has {arg1+points} points available.') 
                                cursor.execute(sql,val) 
                                db.commit()
                                cursor.close()
                                db.close()
                                channel = bot.get_channel(887371257149018153)
                                await channel.send(f"{user.display_name} has been given {arg1} for '{Disc}'")
                        else:
                                await ctx.channel.send(f'{user.name}, are you abusing your power??')
                else:
                        await ctx.channel.send(f'{arg1} is an invalid number.') 





#Remove Points Command
@bot.command()
async def removepoints(ctx, arg1: str, user: discord.Member):
        id = bot.get_guild(877528142909161572)
        channels = ['dkp']
 
        if ctx.message.author.guild_permissions.manage_roles:
                if str(ctx.channel) in channels:
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select Points FROM Points WHERE User_ID = {user.id}")
                        result = cursor.fetchone()
                        points = result[0]
                        arg1 = int(arg1)
                        check = points - arg1
                        if result is not None:
                                print(user.id)
                                print(ctx.message.author.id)
                                sql = ("UPDATE Points SET Points = ? WHERE User_ID = ?")
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
 
        if ctx.message.author.guild_permissions.manage_roles:
                if str(ctx.channel) in channels:
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select Points FROM Points WHERE User_ID = {user.id}")
                        result = cursor.fetchone()
                        points = result[0]
                        check = points - points
                        if result is not None:
                                sql = ("UPDATE Points SET Points = ? WHERE User_ID = ?")
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

        if str(ctx.channel) in channels:
                db = sqlite3.connect('Test.sqlite')
                cursor = db.cursor()
                cursor.execute(f"Select Points FROM Points WHERE User_ID = {ctx.message.author.id}")
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

#RemoveItem Command
@bot.command()
async def RemoveItem(ctx, item):
        id = bot.get_guild(877528142909161572)
        channels = ['dkp']
 
        if ctx.message.author.guild_permissions.send_messages:
                if str(ctx.channel) in channels:
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select Item_ID FROM Items WHERE ItemName = '{item}'")
                        result = cursor.fetchone()
                        if result is None: 
                                await ctx.channel.send(f'That item does not Exists.')
                        elif result is not None:
                                sql = (f"Delete FROM Items Where Item_ID = ?")
                                val = (result[0],)
                                cursor.execute(sql,val)
                                print(f"{item}' deleted item_id' {result[0]} ")
                                db.commit
                                cursor.close()
                                db.close

#store command
@bot.command()
async def Store(ctx): 
        channels = ['dkp']
        if ctx.message.author.guild_permissions.send_messages:
                if str(ctx.channel) in channels:
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select ItemName, cost FROM Items")
                        result = cursor.fetchall()
                        s = ['ItemName        cost']
# This needs to be adjusted based on expected range of values or   calculated dynamically
                        for data in result:
                                s.append('   '.join([str(item).center(10, ' ') for item in data]))
                        d = '```'+'\n'.join(s) + '```'
                        embed = discord.Embed(title = 'Store Inventory', colour=discord.Colour(0x0ECA14), description = d)
                        embed.set_thumbnail(url='https://cdn.discordapp.com/icons/184864850059460609/293ef38d13267880ba274086a16e7593.png?size=32')
                        await ctx.channel.send(embed = embed)

#MyInventory Command
@bot.command()
async def MyInventory(ctx):
    # Example dataset here! 
        channels = ['dkp']
        if ctx.message.author.guild_permissions.send_messages:
                if str(ctx.channel) in channels:
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select ItemName, Count FROM Inventory Where user_ID = {ctx.message.author.id}")
                        result = cursor.fetchall()
                        s = ['ItemName        Count']
                        for data in result:
                                s.append('   '.join([str(item).center(10, ' ') for item in data]))
                        d = '```'+'\n'.join(s) + '```'
                        embed = discord.Embed(title = 'Personal Inventory', colour=discord.Colour(0x0ECA14), description = d)
                        embed.set_thumbnail(url='https://cdn.discordapp.com/icons/184864850059460609/293ef38d13267880ba274086a16e7593.png?size=32')
                        await ctx.channel.send(embed = embed)
                        

#BuyItems Command
@bot.command()
async def BuyItem(ctx, item):
        id = bot.get_guild(877528142909161572)
        channels = ['dkp']
 
        if ctx.message.author.guild_permissions.send_messages:
                if str(ctx.channel) in channels:
                        newcount = 0
                        db = sqlite3.connect('Test.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"Select cost FROM Items WHERE ItemName = '{item}'")
                        price = cursor.fetchone()
                        cursor.execute(f"Select Points FROM Points WHERE User_ID = {ctx.message.author.id}")
                        points = cursor.fetchone()
                        cursor.execute(f"Select Count FROM Inventory WHERE ItemName = '{item}' AND User_ID = {ctx.message.author.id}")
                        itemcount = cursor.fetchone()
                        balance = points[0] - price[0]
                        if price is None:
                                await ctx.channel.send(f'{item} Has Not Been Added To The Store.')
                        elif points is None:
                                await ctx.channel.send(f'You do not have any points')
                        elif balance < 0:
                                await ctx.channel.send(f'You do not have enough points purchase this item.')
                        elif balance >= 0:
                                sql = ("UPDATE Points SET Points = ? WHERE User_ID = ?")
                                val = (balance,ctx.message.author.id) 
                                cursor.execute(sql,val) 
                                db.commit()
                                if itemcount is None:
                                        newcount = 1
                                        sql = ("INSERT INTO Inventory(Guild_iD,Count,ItemName,user_ID) VALUES(?,?,?,?)")
                                        val = (ctx.guild.id,newcount,item,ctx.message.author.id)
                                        cursor.execute(sql,val)  
                                        db.commit()
                                else:   
                                        newcount = itemcount[0]+1
                                        print(newcount)
                                        sql = ("UPDATE Inventory SET Count = ? WHERE ((User_ID = ?) AND (ItemName = ?))")
                                        val = (newcount,ctx.message.author.id,item) 
                                        cursor.execute(sql,val) 
                                        db.commit()
                                cursor.close()
                                db.close()
                                await ctx.channel.send(f'{ctx.message.author.name} has purchased {item} and has {balance} remaining points left. They now have {newcount} {item}(s)') 




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


#on_connect
@bot.event
async def on_connect():
        print('DKP bot is now connected to discord!')

#on_ready
@bot.event
async def on_ready():
        db = sqlite3.connect('Test.sqlite')
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Points(
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
        db = sqlite3.connect('Test.sqlite')
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Inventory( 
                guild_id TEXT,
                Count INTEGER, 
                ItemName TEXT, 
                user_ID INTEGER
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