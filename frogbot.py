import discord
import asyncio
import sys

client = discord.Client()
authTokenLocation = "./token.txt"

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

print("Starting with ", len(sys.argv), " arguments.")
print(str(sys.argv])

getAuthToken = open(authTokenLocation, "r") #opens file with name of "test.txt"
client.run(getAuthToken.read())
sys.exit()
