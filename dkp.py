#Discord Bot for DKP System

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

#Is bot online function
@client.event
async def on_connect():
        print('DKP bot is now connected to discord!')

@client.event
async def on_ready():
        print('DKP system is running')

@client.event
async def on_disconnect():
        print('DKP bot has disconnected from discord')
        
#Hello function
@client.event
async def on_message(message):
    if message.author == client.user:
        return 

    if message.content.startswith('$hello'):
        await message.channel.send ('hello!')

client.run(token)
