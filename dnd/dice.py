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
