import discord
import asyncio
import sys
import random
import configparser

client = discord.Client()

botAuthTokenPath = None
botHomeChannelID = None
botControllerRole = None
botCommandPrefix = None
froggyQuotesPath = None

def getConfiguration():
	global botAuthTokenPath
	global botHomeChannelID
	global botControllerRole
	global botCommandPrefix
	global froggyQuotesPath

	config = configparser.ConfigParser()
	config.read('./bot.conf')

#	config['FROG_CONFIG'] = {'TokenPath': "./token.txt",
#							'BotHomeChannelID': "454470370817343488",
#							'BotControllerRole': "Frog",
#							'BotCommandPrefix': "!",
#							'FroggyQuotesPath': "./resources/frogquotes.txt"
#							}

	bothAuthTokenPath = config['FROG_CONFIG']['TokenPath']
	botHomeChannelID = config['FROG_CONFIG']['BotHomeChannelID']
	botControllerRole = config['FROG_CONFIG']['BotControllerRole']
	botCommandPrefix = config['FROG_CONFIG']['BotCommandPrefix']
	froggyQuotesPath = config['FROG_CONFIG']['FroggyQuotesPath']

def getRandomFroggyQuote():
	return random.choice(open(froggyQuotesPath).read().splitlines())

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
getAuthToken = open(botAuthTokenPath, "r") #opens file at the path of authTokenPath, in read mode
client.run(getAuthToken.read()) # reads the file and uses whatever is in at the auth toeken
sys.exit()