### Functions

def lexicalAnalyzer():
	state = 0
	while (state != -1 or state != -2):
		## Check for ID
		if (state == 0 and input in letters):
			state = 1
		elif (state == 1 and input in letters or input in digits):
			state = 1
		
		## Check for Number
		elif (state == 0 and input in digits):
			state = 2
		elif (state == 2 and input in digits):
			state = 2
			
		## Check for Operator
		elif (state == 0 and input in operator):
			state = -2
		
		## Check for symbol #
		elif (state == 0 and input == "#"):
			state = 3
		elif (state == 3 and input == "#"):
			state = 4
			
			
	  

### Main Program
