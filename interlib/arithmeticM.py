#Clear output file on startup
outputFile = open("psuedo output.py", "w")
outputFile.close()
inputFile = open("psuedo text.txt", "r")
outputFile = open("psuedo output.py", "a")

#mimicking all_variables
allVariables =	{
  "x": 1,
  "y": 2,
  "z": 0,
  "i": 12,
  "foo": 7,
  "neg": -10,
  "day": "Monday",
  "missing": None
}


def add(numList):
	result = 0
	for x in numList:
		if type(x) == int or type(x) == float:
			result = result + x
		else:
			raise Exception("Error, Add function was passed an invalid value")

	return result


def multiply(numList):
	result = 1
	for x in numList:
		if type(x) == int or type(x) == float:
			result = result * x
		else:
			raise Exception("Error, Multiply function was passed an invalid value: " + x)
			
	return result


#basic math function dictionary. add was included to veryify if this could work with other functions
basicMath =	{
  "multiply": multiply,
  "add": add
}


def writeLine(var, function, symbolList):

	if function == "multiply":
		body = " * ".join(symbolList)
		outputFile.write(var + " = " + body + "\n")
	
	elif function == "add":
		body = " + ".join(symbolList)
		outputFile.write(var + " = " + body + "\n")

	else:
		raise Exception("Error, Invalid function")


def variableCheck(var1):
	if var1.replace('.', '', 1).isdigit():
		if var1.isdigit:
			return int(var1)
		else:
			return float(var1)
	else:
		temp = allVariables.get(var1)
		if temp != None:
			return temp
		else:
			raise Exception("Error, Variable not found")


#(Add/Subtract/Multiply/Divide) <variable name> and <variable name>, store [it/the result] into <variablename>
def processMath(line):
	lineParts = line.split()
	function = "NULL"
	var = "NULL"
	counter = 0
	symbolList = []
	numList = []
	reachedStore = False

	for part in lineParts:
		part = part.replace(",", "")      #Remove commas seperating numbers or variables

		if counter == 0:
			function = part.lower()       #First part is function name

		elif counter == len(lineParts)-1:
			var = part                    #variable check here if Math function can not create variables

		else:                            
			if part == "store":
				reachedStore = True

			if not reachedStore:
				if part != "and":
					symbolList.append(part)
					numList.append(variableCheck(part))

		counter+=1

	if reachedStore == False:
		raise Exception("Error, Math function missing Store key word.")

	allVariables[var] = basicMath[function](numList)
	writeLine(var, function, symbolList)


def verifyRequest(line):
	keyWord = line.split()[0]

	if keyWord.lower() in basicMath.keys():
		processMath(line)


def parsePsuedo():
    inputText = inputFile.read().replace('\n', ' ')
    inputText = " ".join(inputText.split())   #removes multiple spaces
    inputText = inputText[:-1]                #removes last period for parsing reasons
    inputParts = inputText.split(". ")
    return inputParts;


def main():
	psuedoLines = parsePsuedo();
	
	for line in psuedoLines:
		verifyRequest(line)

if __name__ == "__main__":
	main()