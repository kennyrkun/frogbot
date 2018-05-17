import discord
import asyncio
import sys
import random

client = discord.Client()
authTokenLocation = "./token.txt"
frogQuotesLocation = ".resources/frogquotes.txt"
botCommandPrefix = "!"

def getRandomFroggyQuote(path):
	return random.choice(open(path).readlines())

@client.event
async def on_ready():
	print('Logged in as:')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	if message.content.startswith(botCommandPrefix + "sins"):
		await client.send_message(message.channel, "I heard Minecraft?")
	
	if message.content.startswith(botCommandPrefix + "frog"):
		#await client.send_message(message.channel, getRandomFroggyQuote(frogQuotesLocation))
		await client.send_message(message.channel, "insert frog quote")

print("Starting with ", len(sys.argv), " arguments.")
print(str(sys.argv))

getAuthToken = open(authTokenLocation, "r") #opens file at the path of authTokenLocation, in read mode
client.run(getAuthToken.read()) # reads the file and uses whatever is in at the auth toeken
sys.exit()
