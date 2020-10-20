'''
Code to help with testing

#Clear output file on startup
outputFile = open("psuedo output.py", "w")
outputFile.close()

outputFile = open("psuedo output.py", "a")

#mimicking all_variables
allVariables =	{
  "x": {"data_type": "number", "value": 1},
  "y": {"data_type": "number", "value": 2},
  "z": {"data_type": "number", "value": 0}
}
'''

def print_line(line_numb, line_list):
  line = ""
  for word in line_list:
    line += word + " "
  print("Line " + str(line_numb) + ': ' + line)


#Checks if var is a number or a variable in all_varaibles
#called for places where var is allowed to be a variable or number
def variableCheck(var, all_variables): 
	if var.replace('.', '', 1).isdigit():
		if var.isdigit:
			return [int(var), True]
		else:
			return [float(var), True]
	else:
		temp = all_variables.get(var)
		if temp != None:
			if temp["data_type"] == "number":
				return [temp["value"], True]
			else:
				return [None, False]
		else:
			return [None, False]

  
def multiply(line_numb, line_list, py_lines, all_variables, indent, py_file):
	var = "NULL"
	counter = 0
	symbolList = []
	numList = []
	reachedStore = False

	for part in line_list:
		part = part.replace(",", "")    

		if counter == 0:
			pass 
		elif counter == len(line_list)-1:
			var = part      

		else:                            
			if part == "store":
				reachedStore = True

			if not reachedStore:
				if part != "and":
					symbolList.append(part)

					varNum = variableCheck(part, all_variables)

					if varNum[1] == False:
						print_line(line_numb, line_list) #"Error, Variable not found"
						return False

					numList.append(varNum[0])

		counter+=1

	if reachedStore == False:
		print_line(line_numb, line_list) #"Error, Math function missing Store key word."
		return False

	result = 1
	for x in numList:
		if type(x) == int or type(x) == float:
			result = result * x
		else:
			print_line(line_numb, line_list) #"Error, Multiply function was passed an invalid value: " + x
			return False
			
	all_variables[var] = {"data_type": "number", "value": result}

	body = " * ".join(symbolList)
	indent_space = indent * " "
	py_line = indent_space + var + " = " + body + "\n"
	py_lines.append(py_line)
	


'''
Code to help with testing

def listToString(s): #Geeks for Geeks
    # initialize an empty string 
    str1 = ""  
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    # return string   
    return str1

def main():
	py_lines = ["someNum = 12\n", "otherNum = 9\n"]
	line_numb = 2
	indent = 4
	line_list1 = ["Multiply", "x", "and", "1,", "store", "it", "into", "z"]
	line_list2 = ["Multiply", "6", "and", "1,", "store", "it", "into", "z"]
	#multiply(line_numb, line_list, py_lines, all_variables, indent, py_file):
	multiply(line_numb, line_list1, py_lines, allVariables, indent, None)
	line_numb+=1
	multiply(line_numb, line_list2, py_lines, allVariables, indent, None)

	outputFile.write(listToString(py_lines))

if __name__ == "__main__":
	main()
'''
