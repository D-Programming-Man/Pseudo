from interlib.utility import inter_data_type
from interlib.utility import print_line

help_manual = "  Syntax: \n" \
              "  Add (<variable name>/<number>) and (<variable name>/<number>), store [it/the result] into <variable name> \n" \
              "  \n" \
              "  Examples: \n" \
              "  Add 1 and 2, store into x \n" \
              "  Add x and 4, store into y \n" \
              "  Add 1.4843 and 3.431, store into w \n" \
              "  Add 1.32 and y, store into z \n" \
              "  Add var_1 and var_2, store into result \n"
              

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

  # Currently variable names are in index 1 and 3. 
  # Check that they exist and are valid data types, or are numbers. i.e "1","1.1"
  # Last element in the list is the variable name we want to add to. 
  # Update the last variable in line_list to all_variables with the sum of the first two
  word_pos = 1
  
  var1_name = line_list[word_pos]
  word_pos += 1
  
  if line_list[word_pos] == "and":
    word_pos += 1
  else:
    print("Expected word \"and\" after first operand.")
    print_line(line_numb, line_list)
    return False
  
  var2_name = line_list[word_pos]
  if var2_name[-1] == ",":
    var2_name = var2_name[0:-1] 
  word_pos += 1
  
  var1_number = is_valid_number(var1_name)
  var2_number = is_valid_number(var2_name)
  
  if var1_number == None:
    data_type = ""
    try: 
      data_type = all_variables[var1_name]["data_type"]
    except:
      print("Variable \"" + var1_name + "\" does not exist.")
      print_line(line_numb, line_list)
      return False
    if data_type == "number":
      var1_number = all_variables[var1_name]["value"]
    else:
      print("Operand \"" + var1_name + "\" has not been created yet.")
      print_line(line_numb, line_list)
      return False
      
  if var2_number == None:
    data_type = ""
    try: 
      data_type = all_variables[var2_name]["data_type"]
    except:
      print("Variable \"" + var2_name + "\" does not exist.")
      print_line(line_numb, line_list)
      return False
    if data_type == "number":
      try:
        var2_number = all_variables[var2_name]["value"]
      except:
        print("Operand \"" + var2_name + "\" has not been created yet.")
        print_line(line_numb, line_list)
        return False
  
  if line_list[word_pos] == "store":
    word_pos += 1
  else:
    print("Expected word \"store\" after second operand.")
    print_line(line_numb, line_list)
    return False
    
  if line_list[word_pos] == "it":
    word_pos += 1
  elif line_list[word_pos] == "the":
    word_pos += 1
    if line_list[word_pos] == "result":
      word_pos += 1
    else:
      print("Expected word \"result\" after the word \"the\".")
      print_line(line_numb, line_list)
      return False

  if line_list[word_pos] == "into":
    word_pos += 1
  else:
    print("Expected word \"into\" after the word \"" + line_list[word_pos - 1] + "\".")
    print_line(line_numb, line_list)
    return False
  
  var3_name = line_list[word_pos]
  temp_sum_val = var1_number + var2_number

  # update or create new entry in dictionary. {"x":{"data_type":"number", "value":#}}
  all_variables[var3_name] = {"data_type": "number", "value": temp_sum_val}

  py_equivalent = " "*indent + var3_name + " = " + var1_name + " + " + var2_name + "\n"
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
    return None
