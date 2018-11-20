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

	botAuthTokenPath = config['FROG_CONFIG']['TokenPath']
	botHomeChannelID = config['FROG_CONFIG']['BotHomeChannelID']
	botControllerRole = config['FROG_CONFIG']['BotControllerRole']
	botCommandPrefix = config['FROG_CONFIG']['BotCommandPrefix']
	froggyQuotesPath = config['FROG_CONFIG']['FroggyQuotesPath']

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

@client.event
async def on_ready():
	print("logged in as " + client.user.name + " (" + client.user.id + ")")
	await client.send_message(client.get_channel(botHomeChannelID), "yea what's up? :white_check_mark:")

@client.event
async def on_message(message):
	print(message.author.name + "#" + message.author.discriminator + ": " +  message.content)

	if message.content.startswith(botCommandPrefix + "help"):
		await client.send_message(message.channel, "List of commands:\n\n`!help` - this dialog.\n`!fcuk` - responds with a random frog quote\n`!roll` - rolls a dice with the specified number of sides\narguments:\nsides: number of sides on the die\nmodifier: DnD modifier\n`!check` - DnD skill check\ninternally calls `!roll 20 [modifier]`")

	if message.content.startswith(botCommandPrefix + "fcuk"):
		await client.send_message(message.channel, getRandomFroggyQuote())
		
#	TODO: this
#	if message.content.startswith(botCommandPrefix + "sins"):
#		await client.send_message(message.channel, "I heard Minecraft?")

	if message.content.startswith(botCommandPrefix + "check"):
		await client.send_message(message.channel, abilityCheck(message.content))
		
	if message.content.startswith(botCommandPrefix + "roll"):
		await client.send_message(message.channel, rollDice(message.content))

#	TODO: add this as a thing for admins
#	if message.content.startswith(botCommandPrefix + "setgame"):
#		await client.send_message(message.channel, "test")
#		await client.change_presence(game=discord.Game(name='something goes here'))

print("Starting with ", len(sys.argv), " arguments.")
print(str(sys.argv))

getConfiguration()
getAuthToken = open(botAuthTokenPath, "r")
client.run(getAuthToken.read())
sys.exit()