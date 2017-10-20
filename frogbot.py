import discord
import asyncio
import sys

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	if message.content.startswith("!sins"):
		await client.send_message(message.channel, "I heard Minecraft?")

f = open("token.txt","r") #opens file with name of "test.txt"
client.run(f.read())
sys.exit()