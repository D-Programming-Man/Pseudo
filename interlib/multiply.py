from interlib.utility import inter_data_type
from interlib.utility import print_line

help_manual = "  Syntax: \n" \
              "  Multiply (<variable name>/<number>) and (<variable name>/<number>), store [it/the result] into <variable name> \n" \
              "  \n" \
              "  Examples: \n" \
              "  Multiply 1 and 2, store into x \n" \
              "  Multiply x and 4, store into y \n" \
              "  Multiply 1.4843 and 3.431, store into w \n" \
              "  Multiply 1.32 and y, store into z \n" \
              "  Multiply var_1 and var_2, store into result \n"

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
def handler(interpret_state):
  line_numb = interpret_state["line_numb"]
  line_list = interpret_state["line_list"]
  all_variables = interpret_state["all_variables"]
  indent = interpret_state["pseudo_indent"] + interpret_state["indent"]
  py_lines = interpret_state["py_lines"]

  var = "NULL"         #Variable to store in
  symbolList = []      #Used to create string to send to py_lines
  numList = []         #Used to calculate values
  reachedAnd = False
  reachedStore = False
  reachedInto = False
  found1Var = False
  found2Var = False
  counter = 0

  for part in line_list:
    part = part.replace("\n", "") #Newlines are not valid characters for variables

    #Since the first part is Multiply we can ignore it
    if counter == 0:
      pass

    #Last part is the varaible we want to store in  
    elif counter == len(line_list)-1:
      var = part

    else:
      if part == "and":
        reachedAnd = True
      elif part == "store":
        reachedStore = True
      elif part == "into":
        reachedInto = True

      # If we have not seen "store" yet then we are adding the variables or numbers we see to lists
      elif not reachedStore:

        if reachedAnd and found2Var: #More than 2 inputs found so far. Third was just found
          print("Error, Bad syntax")
          print_line(line_numb, line_list)
          return False

        # The second variable is reached right after "and" and has a comma after it
        if reachedAnd:
          lastChar = part[-1]
          if lastChar != ",":
            print("Error, missing comma")
            print_line(line_numb, line_list)
            return False
          else:
            part = part[:-1]
          
          found2Var = True
        
        #We are checking if this is the first variable or second
        if found1Var == False or reachedAnd == True:
          symbolList.append(part)
          varNum = variableCheck(part, all_variables)
          if varNum == None:
            print("Error, Variable not found")
            print_line(line_numb, line_list) 
            return False
          numList.append(varNum)
          found1Var = True
        else:
          print("Error, Bad syntax")
          print_line(line_numb, line_list)
          return False

      #Any input outside of the structure will throw an error
      #This is only reached after we have read past "store"
      else:
        if part != "it" and part != "the" and part != "result":
          print("Error, Bad syntax")
          print_line(line_numb, line_list)
          return False

    counter+=1

  #Check if there are missing keywords
  if reachedAnd == False or reachedStore == False or reachedInto == False or found2Var == False:
    print("Error, Bad syntax")
    print_line(line_numb, line_list)
    return False

  #Here we take the list of numbers to multiply and mutlipy them (at the moment it's always 2)
  result = 1
  for x in numList:
    if type(x) == int or type(x) == float:
      result = result * x
    else:
      print("Error, Multiply function was passed an invalid value")
      print_line(line_numb, line_list)
      return False
      
  all_variables[var] = {"data_type": "number", "value": result}

  body = " * ".join(symbolList)
  indent_space = indent * " "
  py_line = indent_space + var + " = " + body + "\n"
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
  new_var = var.replace('.', '', 1)
  new_var = new_var.replace('-', '', 1)
  if new_var.isdigit():
    if var.isdigit():
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