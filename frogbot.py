import discord
import asyncio
import sys
import random

client = discord.Client()

botAuthTokenLocation = None
botCommandPrefix = None
botHomeChannelID = None
botControllerRole = None
froggyQuotesLocation = None

def getConfiguration():
	getConfig = open("./bot.conf", "r")

#	TODO: find a better way to do this
	global botAuthTokenLocation
	botAuthTokenLocation = getConfig.readline().rstrip()
	global botHomeChannelID
	botHomeChannelID  = getConfig.readline().rstrip()
	global botControllerRole
	botControllerRole = getConfig.readline().rstrip()
	global botCommandPrefix
	botCommandPrefix = getConfig.readline().rstrip()
	global froggyQuotesLocation
	froggyQuotesLocation = getConfig.readline().rstrip()

	print("loaded configuration")

def getRandomFroggyQuote():
	return random.choice(open(froggyQuotesLocation).read().splitlines())

@client.event
async def on_ready():
	print("logged in as " + client.user.name + " (" + client.user.id + ")")
	await client.send_message(client.get_channel(botHomeChannelID), "yea what's up? :white_check_mark:")

@client.event
async def on_message(message):
	print(message.author.name + "#" + message.author.discriminator + ": " +  message.content)

	if message.content.startswith(botCommandPrefix + "help"):
		await client.send_message(message.channel, "List of commands:\n\n`!help` - this dialog.\n`!fcuk` - responds with a random frog quote")

#	TODO: this
#	if message.content.startswith(botCommandPrefix + "sins"):
#		await client.send_message(message.channel, "I heard Minecraft?")

	if message.content.startswith(botCommandPrefix + "fcuk"):
		await client.send_message(message.channel, getRandomFroggyQuote())

#	TODO: add this as a thing for admins
#	if message.content.startswith(botCommandPrefix + "setgame"):
#		await client.send_message(message.channel, "test")
#		await client.change_presence(game=discord.Game(name='something goes here'))

print("Starting with ", len(sys.argv), " arguments.")
print(str(sys.argv))

getConfiguration()
getAuthToken = open(botAuthTokenLocation, "r") #opens file at the path of authTokenLocation, in read mode
client.run(getAuthToken.read()) # reads the file and uses whatever is in at the auth toeken
sys.exit()
