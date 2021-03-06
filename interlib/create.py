from interlib.utility import key_var_check
from interlib.utility import print_line
from interlib.utility import list_dict_checker

help_manual = "  Syntax: \n" + \
              "  Create [a/an] <data type> named <variable name> with [a] (value/values) <value> \n" \
              "  \n" \
              "  Examples: \n" \
              "  Create a variable named x with a value 1 \n" \
              "  Create a variable named text with a value \"This is a text\" \n" \
              "  Create a list named new_list with values [1, 2, 3, 4, 5] \n" \
              "  Create a table named new_table with a value {1: \"Text\"} \n" \

# Global so that we don't create this list everytime we run the "Create" keyword
special_characters = ['[', ']', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                        '_', '=', '+', '{', '}', ';', ':', '"', "'", ',', '<', '>',
                        '/', '?', '\\', '|']

# function to parse number values
def num_parse(value_list):

  if value_list[0] == "." or value_list[0] == "-":
    return None
    
  is_negative = False
  period_counter = 0
  char_pos = 0
  for digit in value_list[0]:
    # If we encounter a character that isn't a digit or we have two periods, then it must be a variable name that isn't in the all_variables dictionary. Error out
    if digit.isalpha() or digit in special_characters:
      return None

    # Check if negative signs are in the value
    if digit == "-" and char_pos > 0:
      return None

    # Checking for periods
    if period_counter < 2:
      if digit == ".":
        period_counter += 1
    else:
      return None

    # Rare instance where the period is at the end of the number, for example: 1.3478392784832.
    if period_counter > 1:
      return None
    
    # Need to check position 
    char_pos += 1

  # It must be a valid number
  if period_counter == 0:
    return int(value_list[0])
  else:
    return float(value_list[0])


# function to parse string or multiple spaced string values
def str_parse(multi_string, value_list, quotation_mark):

  if multi_string:

    # Check if the same quotation mark is at the end
    if value_list[-1][-1] == quotation_mark:
      # This is a valid string, return the value
      value = value_list[0][1:] + " "

      for i in range(1, len(value_list) - 1):
        value += value_list[i] + " "
      value += value_list[-1][0:-1]

      return value

    else:
      # Invalid string return False
      return False

  else:

    # Check if the same quotation mark is at the end
    if value_list[0][-1] == quotation_mark:
      return value_list[0][1:-1]
    else:
      return False

'''
 Since we know that this line contains the "Create" keyword, we start at the word after "Create" to check the whole line to create the python equivalent of the phrase or if it contains errors
 
 Requires:
 . line_numb = The line number we are looking at in the Psudo code file
 . line_list = The line we took from the Psudo code file, but in list format
 . all_variables = The dictionary that contains all of the variables for that Psudo code file
 . indent = The indentation to correctly format the line of python code
 . py_lines = The python code that we will append our finalized parsed code to it
 
 Returns:
 . A boolean value. This is used in the interpreter.py file to make sure that the parsing of the code executes correctly. Otherwise the parsing stops and ends it prematurely.
 
'''
def handler(interpret_state):
  line_numb = interpret_state["line_numb"]
  line_list = interpret_state["line_list"]
  all_variables = interpret_state["all_variables"]
  indent = interpret_state["pseudo_indent"] + interpret_state["indent"]
  py_lines = interpret_state["py_lines"]

  # The position of the line_list
  word_pos = 1

  # Ignoring the articles if encountered and move along with the word position
  if line_list[word_pos] == "a" or line_list[word_pos] == "an":
    word_pos += 1

  # Determine if the data type is a variable, list, dictionary, function, or object
  # Remember:
  # Key = variable name, Value = {"data_type": data_type, "value": value}
  data_type = line_list[word_pos].lower()
  word_pos += 1

  # Checks if the next word is "named", if not then display error
  if line_list[word_pos].lower() == "named":
    word_pos += 1
    # Initialize the variable to nothing yet, check to make sure that there is a valid value at the end of the sentence.
    variable_name = line_list[word_pos]
    try:
      if all_variables[variable_name] is not None:
        pass
    except:
      all_variables[variable_name] = None
    word_pos += 1
  else:
    print("Error: The word 'named' is not after the data type.")
    print_line(line_numb, line_list)
    return False

  # Checks if the word after the variable name is "with", if not then display error
  if line_list[word_pos] == "with":
    word_pos += 1
  else:
    print("Error: The word 'with' is not after a single word variable name.")
    print_line(line_numb, line_list)
    return False

  # Ignore articles
  if line_list[word_pos] == "a" or line_list[word_pos] == "an":
    word_pos += 1

  # Checks if the next word is either "value" or "values", if not then display error
  if line_list[word_pos] == "value" or line_list[word_pos] == "values":
    word_pos += 1
  else:
    print("Error: The required parentheses word 'value' or 'values' is not after the 'with' word.")
    print_line(line_numb, line_list)
    return False

  # Get the rest of the list from the line and work from there
  value_list = line_list[word_pos:]

  # The value that we will pass to the all_variables dictionary. Remember:
  # Key = variable name, Value = {"data_type": data_type, "value": value}
  value = None

  # Initialize bools to determine the data type. Could be different from what the user specified. Like, if the user specified a variable but the interpreter determined that the value was a table so there is a confict between data types.
  is_number = False
  is_string = False
  is_boolean = False
  is_variable = False
  is_list = False
  is_dict = False
  multi_string = False

  # If the rest of the list has a length less than 1, then we be sure that it is a number, string, or a variable name
  if len(value_list) < 2:

    # Checking if the value contains a quotation, if so then it's a string
    if value_list[0][0] == '"' or value_list[0][0] == "'":
      quotation_mark = value_list[0][0]
      is_string = True

      # call str_parse to get the value
      value = str_parse(multi_string, value_list, quotation_mark)

      # value was invalid so throw error
      if value == False:
        print("Error: Quotation marks are not the same for the string")
        print_line(line_numb, line_list)
        return False

    # Checking for single entry list
    elif value_list[0][0] == "[":
      is_list = True
      value = list_dict_checker(data_type, all_variables, value_list)
      
      if not data_type == "list":
        print("Error: data type declared is '" + data_type + "' but the data given is a list")
        print_line(line_numb, line_list)
        return False
      
      if value == False:
        print("Error: Invalid list")
        print_line(line_numb, line_list)
        return False
      
    elif value_list[0][0] == "{":
      is_dict = True
      
      value = list_dict_checker(data_type, all_variables, value_list)
      
      if not data_type == "table":
        print("Error: data type declared is '" + data_type + "' but the data given is a table")
        print_line(line_numb, line_list)
        return False

      if value == False:
        print("Error: Invalid table")
        print_line(line_numb, line_list)
        return False

    # Checking for a boolean
    elif value_list[0].lower() == "true" or value_list[0].lower() == "false":
      is_boolean = True
      value = value_list[0].capitalize()

    # If it doesn't have it, then check if the value is a variable name
    else:
      value_list[0] = value_list[0].split()[0]
      is_string = False
      # If the value is in the dictionary of all_variables, then it must be a variable.
      try:
        if all_variables[value_list[0]] is not None:
          is_variable = True
          value = value_list[0]

      # If the variable name isn't in the dictionary, then it must be a number
      except:
        is_number = True

        # calls num_parse to get number value
        value = num_parse(value_list)
        
        # throws error on invalid input
        if value == None:
          print("Error: The variable name \"" + str(value_list[0]) + "\" has not been created yet.")
          print_line(line_numb, line_list)
          return False



  # Data must be a list, dictionary, or a multi-spaced string
  else:

    # Checking if the value contains a quotation, if so then it's a string
    if value_list[0][0] == '"' or value_list[0][0] == "'":
      quotation_mark = value_list[0][0]
      is_string = True
      multi_string = True

      value = str_parse(multi_string, value_list, quotation_mark)
      if value == False:
        print("Error: Quotation marks are not the same for the string")
        print_line(line_numb, line_list)
        return False


    elif value_list[0][0] == "[":
      is_list = True
      value = list_dict_checker(data_type, all_variables, value_list)
      
      if not data_type == "list":
        print("Error: data type declared is '" + data_type + "' but the data given is a list")
        print_line(line_numb, line_list)
        return False

      if value == False:
        print("Error: Invalid list")
        print_line(line_numb, line_list)
        return False

    elif value_list[0][0] == "{":
      is_dict = True
      value = list_dict_checker(data_type, all_variables, value_list)
      
      if not data_type == "table":
        print("Error: data type declared is '" + data_type + "' but the data given is a list")
        print_line(line_numb, line_list)
        return False

      if value == False:
        print("Error: Invalid table")
        print_line(line_numb, line_list)
        return False

    else:
      print("Error: Improper spaces in line")
      print_line(line_numb, line_list)
      return False




  # The spaces needed for this line of code
  indent_space = indent * " "

  # At the end of determining the data value, we need to check it against the data type
  if data_type == "variable":
    if is_number:
      py_line = indent_space + variable_name + " = " + str(value) + "\n"
      py_lines.append(py_line)
      data_type = "number"
    elif is_string:
      py_line = indent_space + variable_name + ' = "' + str(value + '"\n')
      py_lines.append(py_line)
      data_type = "string"
    elif is_boolean:
      py_line = indent_space + variable_name + ' = ' + str(value + '\n')
      py_lines.append(py_line)
      data_type = "boolean"
    elif is_variable:
      py_line = indent_space + variable_name + ' = ' + str(value) + "\n"
      py_lines.append(py_line)
      data_type = all_variables[value]["data_type"]
      value = all_variables[value]["value"]
    else:
      print("Error: data type declared is 'variable' but the expected data is not a 'variable' data type")
      print_line(line_numb, line_list)
      return False



  elif data_type == "list":
    if is_list:
      py_line = indent_space + variable_name + " = " + str(" ".join(value_list)) + "\n"
      py_lines.append(py_line)
    else:
      print("Error: data type declared is 'list' but the expected data is not a 'list' data type")
      print_line(line_numb, line_list)
      return False

  elif data_type == "table":
    if is_dict:
      py_line = indent_space + variable_name + " = " + str(" ".join(value_list)) + "\n"
      py_lines.append(py_line)
    else:
      print("Error: data type declared is 'table' but the expected data is not a 'table' data type")
      print_line(line_numb, line_list)
      return False  
  
  else:
    print("Error: Unknown data type '" + data_type + "' specfied")
    print_line(line_numb, line_list)
    return False

   # Write the variable into the dictionary just in case if the user wants to use it later
  all_variables[variable_name] = {"data_type": data_type, "value": value}

  return True
