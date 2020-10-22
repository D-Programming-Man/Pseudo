from interlib.utility import inter_data_type

# Used for printing out the line that is associated with the error message
# For line_numb, pass in the 
def print_line(line_numb, line_list):
  line = ""
  for word in line_list:
    line += word + " "
  print("Line " + str(line_numb) + ': ' + line)
  
'''
    Main arithmetic functions
    
Requires:
 . line_numb = The line number we are looking at in the Psudo code file
 . line_list = The line we took from the Psudo code file, but in list format
 . all_variables = The dictionary that contains all of the variables for that Psudo code file
 . indent = The indentation to correctly format the line of python code
 . py_file = The output python code file we are writing to
 
 Returns:
 . A boolean value. This is used in the interpreter.py file to make sure that the parsing of the code executes correctly. Otherwise the parsing stops and ends it prematurely.
'''
def add(line_numb, line_list, py_lines, all_variables, indent, py_file):
  # Currently variable names are in index 1 and 3. 
  # Check that they exist and are valid data types, or are numbers. i.e "1","1.1"
  # Last element in the list is the variable name we want to add to. 
  # Update the last variable in line_list to all_variables with the sum of the first two
  expected_keywords = ["and", "store", "into"]
  found_all_keywords = 0
  for index, elem in enumerate(line_list):
    # removing any "," and "\n"
    line_list[index] = elem.strip(',\n')
    if elem in expected_keywords:
      found_all_keywords+=1
  if found_all_keywords != len(expected_keywords):
    # expected keywords did not all show up
    print_line(line_numb, line_list) #"Error, expected keywords missing" will find a better system for this
    return False

  
  var1_name = line_list[1]
  var2_name = line_list[3]
  var1_number = is_valid_number(var1_name)
  var2_number = is_valid_number(var2_name)
  temp_sum_val = 0
  var3_name = line_list[-1]


  # check that variables are valid in all_variables dict
  # if not check if they are valid numbers
  # if both are not true, return error
  if data_type_check(var1_name, all_variables) == "number":
    if data_type_check(var2_name, all_variables) == "number":
      temp_sum_val = all_variables[var1_name]["value"] + all_variables[var2_name]["value"]
    elif var2_number is None:
      # second variable is not in all_variables dict
      # and is not a number
      print_line(line_numb, line_list)  # "Error, variable not found"
      return False
    else:
      # second variable is a number
      temp_sum_val = all_variables[var1_name]["value"] + var2_number
  elif var1_number is None:
    # variable 1 is not in all_variables dict
    # and is not a number
    print_line(line_numb, line_list)  # "Error, variable not found"
    return False
  else:
    # variable 1 is a number
    if data_type_check(var2_name, all_variables) == "number":
      temp_sum_val = var1_number + all_variables[var2_name]["value"]

    elif var2_number is None:
      # variable 2 is not in all_variables dict
      # and not a number
      print_line(line_numb, line_list)  # "Error, variable not found"
      return False
    else:
      temp_sum_val = var1_number + var2_number

  # update or create new entry in dictionary. {"x":{"data_type":"number", "value":#}}
  all_variables[var3_name] = {"data_type": "number", "value": temp_sum_val}

  py_equivalent = " "*indent + var3_name + " = " + var1_name + " + " + var2_name + "\n"
  py_lines.append(py_equivalent)

  return True
  
def subtract(line_numb, line_list, py_lines, all_variables, indent, py_file):
  
  # Currently variable names are in index 1 and 3.
  # Check that they exist and are valid data types, or are numbers. i.e "1","1.1"
  # Last element in the list is the variable name we want to subtract to.
  # Update the last variable in line_list to all_variables with the difference of the first two
  expected_keywords = ["from", "store", "into"]
  found_all_keywords = 0
  for index, elem in enumerate(line_list):
    # removing any "," and "\n"
    line_list[index] = elem.strip(',\n')
    if elem in expected_keywords:
      found_all_keywords += 1
  if found_all_keywords != len(expected_keywords):
    # expected keywords did not all show up
    # "Error, expected keywords missing" will find a better system for this
    #print_line(line_numb, line_list)
    return False

  var1_name = line_list[1]
  var2_name = line_list[3]
  # will return a dictionary if it is a float, with the length of decimal place
  # so we can know where to round to
  var1_number = is_valid_number(var1_name)
  var2_number = is_valid_number(var2_name)
  
  temp_difference_val = 0
  var3_name = line_list[-1]

  # check that variables are valid in all_variables dict
  # if not check if they are valid numbers
  # if both are not true, return error
  if data_type_check(var1_name, all_variables) == "number":
    if data_type_check(var2_name, all_variables) == "number":
      temp_difference_val = all_variables[var2_name]["value"] - \
          all_variables[var1_name]["value"]
    elif var2_number is None:
      # second variable is not in all_variables dict
      # and is not a number
      #print_line(line_numb, line_list)  # "Error, variable not found"
      return False
    else:
      # second variable is a number
      temp_difference_val = var2_number - all_variables[var1_name]["value"]
  elif var1_number is None:
    # variable 1 is not in all_variables dict
    # and is not a number
    #print_line(line_numb, line_list)  # "Error, variable not found"
    return False
  else:
    # variable 1 is a number
    if data_type_check(var2_name, all_variables) == "number":

      temp_difference_val = all_variables[var2_name]["value"] - var1_number 

    elif var2_number is None:
      # variable 2 is not in all_variables dict
      # and not a number
      #print_line(line_numb, line_list)  # "Error, variable not found"
      return False
    else:
      temp_difference_val = var2_number - var1_number

  # rounding depending on a floats decimal place length
  var1_decimals = var1_name[::-1].find('.')
  var2_decimals = var2_name[::-1].find('.')
  if(var1_decimals >= var2_decimals and var1_decimals >= 0):
    temp_difference_val = round(temp_difference_val, var1_decimals)
    
  elif var2_decimals >= 0:
    temp_difference_val = round(temp_difference_val, var2_decimals)
  
  
  # update or create new entry in dictionary. {"x":{"data_type":"number", "value":#}}
  all_variables[var3_name] = {"data_type": "number", "value": temp_difference_val}
  py_equivalent = indent*" " + var3_name + \
      " = " + var2_name + " - " + var1_name + "\n"
      
  py_lines.append(py_equivalent)

  return True
  
def multiply(line_numb, line_list, py_lines, all_variables, indent, py_file):
  var = "NULL"         #Variable to store in
  symbolList = []      #Used to create string to send to py_lines
  numList = []         #Used to calculate values
  reachedStore = False
  counter = 0

  for part in line_list:
    part = part.replace(",", "")    

    #Since the first part is Multiply we can ignore it
    if counter == 0:
      pass

    #Last part is the varaible we want to store in  
    elif counter == len(line_list)-1:
      var = part      

    else:
      if part == "store":
        reachedStore = True

      # If we have not seen "store" yet then we are adding the variables or numbers we see to lists
      if not reachedStore:
        if part != "and":
          symbolList.append(part)
          
          varNum = variableCheck(part, all_variables)
          if varNum == None:
            print_line(line_numb, line_list) #"Error, Variable not found"
            return False

          numList.append(varNum)

    counter+=1

  #If there was no "store" keyword then this is not a proper format for multiply
  if reachedStore == False:
    print_line(line_numb, line_list) #"Error, Math function missing Store key word."
    return False

  #Here we take the list of numbers to multiply and mutlipy them
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

def divide(line_numb, line_list, py_lines, all_variables, indent, py_file):
  var1 = line_list[1]
  var2 = line_list[3]
  offset = 0
  
  #length check: prevents access errors
  if(len(line_list)<7):
    print("Error on line " + str(line_numb) + ". Missing arguments, refer to divide usage.")
    print_line(line_numb, line_list)
    return False  
  #error check: makes sure var1 exists or is a number
  if(inter_data_type(var1)!="number" and all_variables.get(var1)==None):
    print("Error on line " + str(line_numb) + ". Create "+var1+" before using divide")
    print_line(line_numb, line_list)
    return False   
  #format check: maintains Pseudo format
  if(line_list[2] != "by"):
    print("Error on line " + str(line_numb) + ". Expected \"by\" after first input")
    print_line(line_numb, line_list)
    return False
  #error check: makes sure var2 exists or is a number
  if(inter_data_type(var2)!="number" and all_variables.get(var2)==None):
    print("Error on line " + str(line_numb) + ". Create "+var2+" before using divide")
    print_line(line_numb, line_list)
    return False   

  #initialize values for var1 and var2, to be used in finding value
  var1_value = all_variables.get(var1)
  if(var1_value == None):
    if(var1.isdigit()):
       var1_value = int(var1)
    else:
      var1_value = float(var1)
  else:
    var1_value = all_variables[var1]["value"]

  var2_value = all_variables.get(var2)
  if(var2_value == None):
    if(var2.isdigit()):
       var2_value = int(var2)
    else:
      var2_value = float(var2)
  else:
    var2_value = all_variables[var2]["value"]


  #format check: maintains Pseudo format
  if(line_list[4]!="store"):
    print("Error on line " + str(line_numb) + ". Expected \"store\" after second input")
    print_line(line_numb, line_list)
    return False
  #format check: maintains Pseudo format. updates offset
  if(line_list[5]=="it"):
    offset=1
  elif(line_list[5]=="the"):
    if(line_list[6]=="result"):
      offset = 2
    else:
      print("Error on line " + str(line_numb) + ". Expected \"result\" after \"the\" ")
      print_line(line_numb, line_list)
      return False
  #length check: prevents access errors, updated now that offset is known
  if(len(line_list)<7+offset):
    print("Error on line " + str(line_numb) + ". Missing arguments, refer to divide usage.")
    print_line(line_numb, line_list)
    return False  
  #format check: maintains Pseudo format
  if(line_list[5+offset]!="into"):
    print("Error on line " + str(line_numb) + ". Expected \"into\" before destination variable")
    print_line(line_numb, line_list)
    return False

  var3 = line_list[6+offset]
  var3 = var3[:-1]
  if(inter_data_type(var3)!="number"):
    all_variables[var3] = {"data_type":"number","value":var1_value/var2_value}
  else:
    print("Error on line " + str(line_numb) + ". Expected "+var3+" to be a variable name")
    print_line(line_numb, line_list)
    return False      
  
  py_line = indent*" " + var3 + " = " + var1 + "/" + var2 +"\n"
  py_lines.append(py_line)
  return True




# Helper functions I(Dvir) use, final version might not need these
def is_valid_number(element):
  # Will either return the string as an integer or float, both valid, or return None
  if element.isnumeric():
    return int(element)
  try:
    float(element)
    return float(element)
  except:
   pass


def data_type_check(name, all_variables):
  # if it exists, returns data type
  # else None
  if name in all_variables:
    return all_variables[name]["data_type"]
  else:
    pass

#Helper function for Multiply
#Checks if var is a number or a variable in all_varaibles
#This is called for places where var is allowed to be a variable or a number
def variableCheck(var, all_variables): 
  if var.replace('.', '', 1).isdigit():
    if var.isdigit:
      return int(var)
    else:
      return float(var)
  else:
    temp = all_variables.get(var)
    if temp != None:
      if temp["data_type"] == "number":
        return temp["value"]
      else:
        return None
    else:
      return None