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

def abilityCheck(message):
		string = message.split()

		arg1 = "!roll"
		arg2 = "20"
		arg3 = "0"
		
		# set modifier if we have one
		try:
			arg3 = string[1]
		except IndexError:
			# arg3 default sot zero
			print("no modifer was provided")
		
		# isn't it cool that I'm not duplicating the code here anymore?
		return rollDice(arg1 + " " + arg2 + " " + arg3)
		
def rollDice(message):
	string = message.split()

	if len(string) > 1:
		dieSides = 20

		try:
			dieSides = int(string[1])
		except IndexError:
			dieSides = 20
		
		modifier = 0

		try:
			modifier = int(string[2])
		except IndexError:
			modifier = 0

		roll = random.randint(1, dieSides)

		naturalRoll = False

		# natural roll is highest number without modifier
		# e.g. 20
		if roll == dieSides:
			naturalRoll = True
		else:
			if modifier == 0:
				if roll == 1:
					naturalRoll = True
			
			roll += modifier

			if roll > dieSides:
				roll = dieSides

		returnMessage = "nil"

		if naturalRoll:
			returnMessage = str(roll) + " natural"
		else:
			if modifier > 0:
				returnMessage = str(roll) + " (mod: " + str(modifier) + ")"
			else:
				returnMessage = roll
	else:
		returnMessage = "please specify amount of sides"

	return returnMessage

def percent():
	return random.randint(0, 100)

@client.event
async def on_ready():
#	print("logged in as " + client.user.name + " (" + client.user.id + ")")
	await client.change_presence(game=discord.Game(name = "froggy being a fool", type = 3))
	
	try:
		servers = list(client.servers)
		for x in range(len(servers)):
			channel = client.get_channel(getServerConfigOption(str(servers[x].id), 'BotHomeChannelID'))
			await client.send_message(channel, "yea what's up? :white_check_mark: (v" + str(botVersion) + ")")
	except Exception as exception:
		await client.send_message(client.get_channel(botHomeChannelID), ":bangbang: Exception in on_ready: `" + exception.__class__.__name__ + '`:\n```' + str(exception) + "```")
		return

@client.event
async def on_server_join(server):
	try:
		for c in server.channels:
			if not c.type == discord.ChannelType.text:
				if not c.permissions_for(server.me).send_messages:
					continue
				
		await client.send_message(c, "yea what's up? :white_check_mark: (v" + str(botVersion) + ")")
		
	# TODO: include more information about server
	except Exception as exception:
		await client.send_message(client.get_channel(botHomeChannelID), ":bangbang: Exception in on_server_join: `" + exception.__class__.__name__ + '`:\n```' + str(exception) + "```" + "\nserver: " + server.id)
		return

@client.event
async def on_message(message):
	try:
		#try:
		#	print(message.user.name + "#" + message.user.discriminator + ": " + message.message)
		#except:
		#	print(message.user.id + " does not want to be printed in the terminal!")
			
		if message.content.startswith(botCommandPrefix + "help"):
			await client.send_message(message.channel, "List of commands:\n\n`!help` - this dialog.\n`!fcuk` - responds with a random frog quote\n`!roll` - rolls a dice with the specified number of sides\narguments:\nsides: number of sides on the die\nmodifier: DnD modifier\n`!check` - DnD skill check\ninternally calls `!roll 20 [modifier]`\n`!percent` - random percent between 0 and 100.\n`!setplaying` - sets the playing status for the bot\n\nfrogbot version " + str(botVersion))
#			await client.send_message(message.channel, "List of commands:\n\n`!help` - this dialog.\n`!fcuk` - responds with a random frog quote\n`!roll` - rolls a dice with the specified number of sides\narguments:\nsides: number of sides on the die\nmodifier: DnD modifier\n`!check` - DnD skill check\ninternally calls `!roll 20 [modifier]`\n`!percent` - random percent between 0 and 100.\n`!setplaying` - sets the playing status for the bot\n`!restart` - restarts the bot\n\nfrogbot version " + str(botVersion))
			return

		if message.content.startswith(botCommandPrefix + "fcuk"):
			await client.send_message(message.channel, getRandomFroggyQuote())
			return

	#	TODO: this
	#	if message.content.startswith(botCommandPrefix + "sins"):
	#		await client.send_message(message.channel, "I heard Minecraft?")
	#		return

		if message.content.startswith(botCommandPrefix + "check"):
			await client.send_message(message.channel, abilityCheck(message.content))
			return

		if message.content.startswith(botCommandPrefix + "roll"):
			await client.send_message(message.channel, rollDice(message.content))
			return

		if message.content.startswith(botCommandPrefix + "percent"):
			await client.send_message(message.channel, str(percent()) + "%")
			return

	#	TODO: restrict this to admins
	#	TODO: !setwatching
		if message.content.startswith(botCommandPrefix + "setplaying"):
			# strip the first word
			string = message.content.split(' ', 1) # skip first word ("!setplaying")
			
			try:
				await client.send_message(message.channel, "aye")
				gameName = string[1]

				if gameName == "none":
					await client.change_presence(game=discord.Game(name="froggy being a fool", type=3))
				else:
					await client.change_presence(game=discord.Game(name=gameName, type=3))
			except IndexError:
				await client.send_message(message.channel, "no game name provided")
				
			return
			
#		if message.content.startswith("!restart"):
#			await client.send_message(message.channel, "bye bye :wave::skin-tone-2:")
			
#			os.fsync()
			
#			os.execv("./frogbot.py", sys.argv)
#			sys.exit()
#			return
			
	except Exception as exception:
		await client.send_message(message.channel, ":bangbang: Exception in on_message: `" + exception.__class__.__name__ + '`:\n```' + str(exception) + "```")
		return

print("Starting with ", len(sys.argv), " arguments.")
print(str(sys.argv))

os.chdir(workingPath)

getBotConfiguration()
getAuthToken = open(botAuthTokenPath, "r")
client.run(getAuthToken.read())
sys.exit()
