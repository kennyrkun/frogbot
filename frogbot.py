import discord
import asyncio
import sys
import random

client = discord.Client()
authTokenLocation = "./token.txt"
frogQuotesLocation = ".resources/frogquotes.txt"
botCommandPrefix = "!"

def getRandomFroggyQuote():	
	return random.choice(open(frogQuotesLocation).readlines())

@client.event
async def on_ready():
	print("logged in as " + client.user.name + "(" + client.user.id + ")")

@client.event
async def on_message(message):
	print("rec: " + message.content)

	if message.content.startswith(botCommandPrefix + "sins"):
		await client.send_message(message.channel, "I heard Minecraft?")
	
	if message.content.startswith(botCommandPrefix + "fcuk"):
		await client.send_message(message.channel, getRandomFroggyQuote())

print("Starting with ", len(sys.argv), " arguments.")
print(str(sys.argv))

getAuthToken = open(authTokenLocation, "r") #opens file at the path of authTokenLocation, in read mode
client.run(getAuthToken.read()) # reads the file and uses whatever is in at the auth toeken
sys.exit()
