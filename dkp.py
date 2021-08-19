#Discord Bot for DKP System

#imports
import discord
import logging

#test

#Variables
client = discord.Client() 
logger = logging.getLogger('discord')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

#Logging Function
logger.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler) 


#Hello Function
@client.event
async def on_ready():
        print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return 

    if message.content.startswith('$hello'):
        await message.channel.send ('hello!')

#Token
client.run('ODc3Mjg5ODQyMzY1NTgzMzcw.YRwd1Q.N4ENEPKpl5x2HeGS80csW6hOUnA')
