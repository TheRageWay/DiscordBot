#Discord Bot for DKP System

#test server id = 877528142909161572

#Token
def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

#Imports
import discord
import logging

#Variables
client = discord.Client() 
token = read_token()
logger = logging.getLogger('discord')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

#Logging Function
logger.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler) 

#on_connect
@client.event
async def on_connect():
        print('DKP bot is now connected to discord!')

#on_ready
@client.event
async def on_ready():
        print('DKP system is running')

#on_disconnect
@client.event
async def on_disconnect():
        print('DKP bot has disconnected from discord')

#on_message
@client.event
async def on_message(message):
        id = client.get_guild(877528142909161572)
        if message.author == client.user:
                return 

        if message.content.startswith('$hello'):
                await message.channel.send ('hello!')

        if message.content == "$users":
                await message.channel.send(f"# of Users: {id.member_count}")

client.run(token)
