from interlib.utility import inter_data_type
from interlib.utility import print_line

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
  indent = interpret_state["indent"]
  py_lines = interpret_state["py_lines"]

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
    print("Error on line " + str(line_numb) + ". Incorrect syntax")
    print_line(line_numb, line_list)
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
      print("Error on line " + str(line_numb) + ". Variable not found")
      print_line(line_numb, line_list)
      return False
    else:
      # second variable is a number
      temp_difference_val = var2_number - all_variables[var1_name]["value"]
  elif var1_number is None:
    # variable 1 is not in all_variables dict
    # and is not a number
    print("Error on line " + str(line_numb) + ". Variable not found")
    print_line(line_numb, line_list)
    return False
  else:
    # variable 1 is a number
    if data_type_check(var2_name, all_variables) == "number":

      temp_difference_val = all_variables[var2_name]["value"] - var1_number 

    elif var2_number is None:
      # variable 2 is not in all_variables dict
      # and not a number
      print("Error on line " + str(line_numb) + ". Variable not found")
      print_line(line_numb, line_list)
      return False
    else:
      temp_difference_val = var2_number - var1_number

  # rounding depending on a floats decimal place length if either variable passed in is a float
  var1_decimals = var1_name[::-1].find('.')
  var2_decimals = var2_name[::-1].find('.')
  if(var1_decimals >= var2_decimals and var1_decimals >= 0):
    temp_difference_val = round(temp_difference_val, var1_decimals)
    
  elif var2_decimals >= 0:
    temp_difference_val = round(temp_difference_val, var2_decimals)
  
  
  # update or create new entry in dictionary. {"x":{"data_type":"number", "value":#}}
  all_variables[var3_name] = {"data_type": "number", "value": temp_difference_val}
  py_equivalent = indent*" " + var3_name + " = " + var2_name + " - " + var1_name + "\n"
      
  py_lines.append(py_equivalent)

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