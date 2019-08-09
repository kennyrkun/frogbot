from dnd import dice

import discord

import asyncio
import sys
import os
import random
import configparser

client = discord.Client()
botConfig = configparser.ConfigParser()
config = configparser.ConfigParser()

botVersion = "6.2.2"

botAuthTokenPath = None
botHomeChannelID = None
botControllerRole = None
botCommandPrefix = None
froggyQuotesPath = None

workingPath = "./"

# create and save configuration files for each server when it joins them

def getBotConfiguration():
	global botAuthTokenPath
	global botHomeChannelID
	global botControllerRole
	global botCommandPrefix
	global froggyQuotesPath

	botConfig.read('./bot.conf')

#	config['FROG_CONFIG'] = {'TokenPath': "./token.txt",
#							'BotHomeChannelID': "454470370817343488",
#							'BotControllerRole': "Frog",
#							'BotCommandPrefix': "!",
#							'FroggyQuotesPath': "./resources/frogquotes.txt"
#							}

	botAuthTokenPath = botConfig['FROG_CONFIG']['BotAuthTokenPath']
	botHomeChannelID = botConfig['FROG_CONFIG']['BotHomeChannelID']
	botControllerRole = botConfig['FROG_CONFIG']['BotControllerRole']
	botCommandPrefix = botConfig['FROG_CONFIG']['BotCommandPrefix']
	froggyQuotesPath = botConfig['FROG_CONFIG']['FroggyQuotesPath']

def getBotConfigOption(option):
	return botConfig['FROG_CONFIG'][option]

def getServerConfigOption(serverID, option):
	config = configparser.ConfigParser()
	config.read("server_configurations/" + serverID + ".conf")
	return config[serverID][option]

def getRandomFroggyQuote():
	return random.choice(open(froggyQuotesPath).read().splitlines())

def percent():
	return random.randint(0, 100)

@client.event
async def on_ready():
	print("logged in as " + client.user.name + " (" + client.user.id + ")")
	await client.change_presence(game=discord.Game(name = "froggy being a fool", type = 3))
	
	try:
		servers = list(client.servers)
		for x in range(len(servers)):
			channel = client.get_channel(getServerConfigOption(str(servers[x].id), 'BotHomeChannelID'))
			await channel.send("yea what's up? :white_check_mark: (v" + str(botVersion) + ")")
	except Exception as exception:
		await client.get_channel(botHomeChannelID).send(":bangbang: Exception in on_ready: `" + exception.__class__.__name__ + '`:\n```' + str(exception) + "```")
		return

@client.event
async def on_server_join(server):
	try:
		for c in server.channels:
			if not c.type == discord.ChannelType.text:
				if not c.permissions_for(server.me).sends:
					continue
				
		#await client.send(c, "yea what's up? :white_check_mark:")
		
	# TODO: include more information about server
	except Exception as exception:
		await client.get_channel(botHomeChannelID).send(":bangbang: Exception in on_server_join: `" + exception.__class__.__name__ + '`:\n```' + str(exception) + "```" + "\nserver: " + server.id)
		return

@client.event
async def on_message(message):
	try:
		channel = message.channel

		#try:
		#	print(message.user.name + "#" + message.user.discriminator + ": " + message.message)
		#except:
		#	print(message.user.id + " does not want to be printed in the terminal!")
			
		if message.content.startswith(botCommandPrefix + "help"):
			await channel.send("List of commands:\n\n`!help` - this dialog.\n`!fcuk` - responds with a random frog quote\n`!roll` - rolls a dice with the specified number of sides\narguments:\nsides: number of sides on the die\nmodifier: DnD modifier\n`!check` - DnD skill check\ninternally calls `!roll 20 [modifier]`\n`!percent` - random percent between 0 and 100.\n`!setplaying` - sets the playing status for the bot\n\nfrogbot version " + str(botVersion))
#			await client.send(message.channel, "List of commands:\n\n`!help` - this dialog.\n`!fcuk` - responds with a random frog quote\n`!roll` - rolls a dice with the specified number of sides\narguments:\nsides: number of sides on the die\nmodifier: DnD modifier\n`!check` - DnD skill check\ninternally calls `!roll 20 [modifier]`\n`!percent` - random percent between 0 and 100.\n`!setplaying` - sets the playing status for the bot\n`!restart` - restarts the bot\n\nfrogbot version " + str(botVersion))
			return
		elif message.content.startswith(botCommandPrefix + "fcuk"):
			await channel.send(getRandomFroggyQuote())
			return
	#	TODO: this
	#	if message.content.startswith(botCommandPrefix + "sins"):
	#		await client.send(message.channel, "I heard Minecraft?")
	#		return
		elif message.content.startswith(botCommandPrefix + "check"):
			await message.channel.send(abilityCheck(message.content))
			return
		elif message.content.startswith(botCommandPrefix + "roll"):
			await message.channel.send(rollDice(message.content))
			return
		elif message.content.startswith(botCommandPrefix + "percent"):
			await channel.send(str(percent()) + "%")
			return
	#	TODO: restrict this to admins
	#	TODO: !setwatching
		elif message.content.startswith(botCommandPrefix + "setplaying"):
			# strip the first word
			string = message.content.split(' ', 1) # skip first word ("!setplaying")
			
			try:
				await channel.send("aye")
				gameName = string[1]

				if gameName == "none":
					await client.change_presence(game=discord.Game(name="froggy being a fool", type=3))
				else:
					await client.change_presence(game=discord.Game(name=gameName, type=3))
			except IndexError:
				await channel.send("no game name provided")
				
			return
#		else if message.content.startswith("!restart"):
#			await client.send(message.channel, "bye bye :wave::skin-tone-2:")
			
#			os.fsync()
			
#			os.execv("./frogbot.py", sys.argv)
#			sys.exit()
#			return
#		else:
#			await client.send(message.channel, "what")
	except Exception as exception:
		await channel.send(":bangbang: Exception in on_message: `" + exception.__class__.__name__ + '`:\n```' + str(exception) + "```")
		return

print("Starting with ", len(sys.argv), " arguments.")
print(str(sys.argv))

os.chdir(workingPath)

getBotConfiguration()
getAuthToken = open(botAuthTokenPath, "r")
client.run(getAuthToken.read())
sys.exit()
