# Used for printing out the line that is associated with the error message
def print_line(line_numb, line_list):
  line = ""
  for word in line_list:
    line += word + " "
  print("Line " + str(line_numb) + ': ' + line)
'''
 Since we know that this line contains the "Create" keyword, we start at the word after "Create" to check the whole line to create the python equivalent of the phrase or if it contains errors
 
 Requires:
 . line_numb = The line number we are looking at in the Psudo code file
 . line_list = The line we took from the Psudo code file, but in list format
 . all_variables = The dictionary that contains all of the variables for that Psudo code file
 . indent = The indentation to correctly format the line of python code
 . py_file = The output python code file we are writing to
 
 Returns:
 . A boolean value. This is used in the interpreter.py file to make sure that the parsing of the code executes correctly. Otherwise the parsing stops and ends it prematurely.
 
'''
def handler(line_numb, line_list, py_lines, all_variables, indent, py_file):
  
  # The position of the line_list
  word_pos = 1
  
  # Ignoreing the articles if encountered and move along with the word position
  if line_list[word_pos] == "a" or line_list[word_pos] == "an":
    word_pos += 1
  
  # Determine if the data type is a variable, list, dictionary, function, or object
  # Remember:
  # Key = variable name, Value = {"data_type": data_type, "value": value}
  data_type = ""
  if line_list[word_pos].lower() == "variable":
    data_type = "variable"
    word_pos += 1
  elif line_list[word_pos].lower() == "list":
    data_type = "list"
    word_pos += 1
  elif line_list[word_pos].lower() == "table":
    data_type = "table"
    word_pos += 1
  ### IMPLEMENT LATER
  #elif line_list[word_pos].lower() == "function"
  #  data_type = "function"
  #  word_pos += 1
  
  # Checks if the next word is "named", if not then display error
  if line_list[word_pos].lower() == "named":
    word_pos += 1
    # Initialize the variable to nothing yet, check to make sure that there is a vaild value at the end of the sentence.
    varaible_name = line_list[word_pos]
    try:
      if all_variables[varaible_name] is not None:
        pass
    except:
      all_variables[varaible_name] = None
    word_pos += 1
  else:
    print("Error on line " + str(line_numb) + ". The word 'named' is not after the data type.")
    print_line(line_numb, line_list)
    return False
    
    # Checks if the word after the variable name is "with", if not then display error
  if line_list[word_pos] == "with":
    word_pos += 1
  else:
    print("Error on line " + str(line_numb) + ". The word 'with' is not after a signle word variable name.")
    print_line(line_numb, line_list)
    return False
         
  # Ignore articles
  if line_list[word_pos] == "a" or line_list[word_pos] == "an":
    word_pos += 1
        
  # Checks if the next word is either "value" or "values", if not then display error
  if line_list[word_pos] == "value" or line_list[word_pos] == "values":
    word_pos += 1
  else:
    print("Error on line " + str(line_numb) + ". The required parentheses word 'value' or 'values' is not after the 'with' word.")
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
  is_variable = False
  is_list = False
  is_dict = False
        
  # If the rest of the list has a length less than 1, then we be sure that it is a number, string, or a variable name
  if len(value_list) < 2:
    is_list = False
    is_dict = False
          
    # Checking if the value contains a quotation, if so then it's a string
    if value_list[0][0] == '"' or value_list[0][0] == "'":
      quotation_mark = value_list[0][0]
      is_number = False
      is_variable = False
      
      # Case where the newline character is part of the string
      if value_list[0][-1] == "\n":
        value_list[0] = value_list[0][0:-1]
        
      # Check if the same quotation mark is at the end  
      if value_list[0][-1] == quotation_mark:
        is_string = True
        value = value_list[0][1:-1]
      else:
        print("Error on line " + str(line_numb) + ". Quotation marks are not the same for the string")
        print_line(line_numb, line_list)
        return False
          
    # If it doesn't have it, then check if the value is a variable name
    else:
      value_list[0] = value_list[0].split()[0]
      # If the value is in the dictionary of all_variables, then it must be a variable.
      try:
        if all_variables[value_list[0]] is not None:
          is_number = False
          is_variable = True
          value = value_list[0]

      # If the variable name isn't in the dictionary, then it must be a number
      except:
        is_variable = False
        period_counter = 0
        for digit in value_list[0]:
          # If we encounter a character that isn't a digit or we have two periods, then it must be a variable name that isn't in the all_variables dictionary. Error out
          if digit.isalpha():
            print("Error on line " + str(line_numb) + ". The variable name has not been created yet.")
            print_line(line_numb, line_list)
            return False
              
          # Checking for periods
          if period_counter < 2:
            if digit == ".":
              period_counter += 1
          else:
            print("Error on line " + str(line_numb) + ". The variable name has not been created yet.")
            print_line(line_numb, line_list)
            return False
            
          # Rare instance where the period is at the end of the number, for example: 1.3478392784832.
          if period_counter > 1:
            print("Error on line " + str(line_numb) + ". The variable name has not been created yet.")
            print_line(line_numb, line_list)
            return False
                    
        # It must be a vaild number
        is_number = True
        if period_counter == 0:
          value = int(value_list[0])
        else:
          value = float(value_list[0])
          
  # Data must be a list, dictionary, or a multi-spaced string
  else:
    is_number = False
    is_variable = False
    
    # Checking if the value contains a quotation, if so then it's a string
    if value_list[0][0] == '"' or value_list[0][0] == "'":
      quotation_mark = value_list[0][0]
      is_number = False
      is_variable = False
      
      # Case where the newline character is part of the string
      if value_list[-1][-1] == "\n":
        value_list[-1] = value_list[-1][0:-1]
      
      # Check if the same quotation mark is at the end
      if value_list[-1][-1] == quotation_mark:
        is_string = True
        value = value_list[0][1:] + " "
        for i in range(1, len(value_list) - 1):
          value += value_list[i] + " "
        value += value_list[-1][0:-1]
      else:
        print("Error on line " + str(line_numb) + ". Quotation marks are not the same for the string")
        print_line(line_numb, line_list)
        return False
    
    # TODO: Make it successfully parse list and dictionaries
    
    
    
    
        
      
  # The spaces needed for this line of code
  indent_space = indent * " "
      
  # At the end of determining the data value, we need to check it against the data type
  if data_type == "variable":
    if is_number:
      py_line = indent_space + varaible_name + " = " + str(value) + "\n"
      py_lines.append(py_line)
    elif is_string:
      py_line = indent_space + varaible_name + ' = "' + str(value + '"' + "\n")
      py_lines.append(py_line)
    elif is_variable:
      py_line = indent_space + varaible_name + ' = ' + str(value) + "\n"
      py_lines.append(py_line)
      value = all_variables[value]["value"]
    else:
      print("Error: data type declared is 'variable' but the expected data is not a 'variable' data type")
      print_line(line_numb, line_list)
      return False
      
    # Write the variable into the dictionary just in case if the user wants to use it later
    all_variables[varaible_name] = {"data_type": data_type, "value": value}

  return True