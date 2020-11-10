from interlib.utility import inter_data_type
from interlib.utility import print_line
  
'''
  The handler to display things on the console

Requires:
 . lines_to_write = The list we write the current parsed line to
 . line_list = The line we took from the Psudo code file, but in list format
 . py_lines = A list of lines that will be printed to the python file
              Append newlines to this list
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

  word_pos = 1
  indent_space = indent * " "
    
  # Combine all of the words in the list to 1 long string
  print_values  = ""
  for i in range(word_pos, len(line_list)):
    print_values += line_list[i] + " "
    
  # Add a hidden comma to terminate the last element in the list
  # Look at the next for-loop to understand why we need this
  print_values = print_values[0:-1] + ","
  
  # Each entry is a dictionary that contains a data type and value:
  # For example, {"data_type": "string", "value": "Hello World"}
  # Another example, {"data_type": "variable", "value": x}
  value_list = []
  
  # We are going to build each variable or string by a character. 
  value = ""
  quotation_mark = ""
  previous_char = ""
  
  # Flags
  is_in_string = False
  is_string = False
  is_variable_name = True   # Assume we're always build variable names
                            # Sort of misleading because we are including
                            # integers and floats into this catagory.
                            # Essentially, it's a 'not_string' boolean
  can_add_to_list = False
  
  # Go through each character and determine if it is a string or a variable
  for char in print_values:
    if char == '"' or char == "'":
      if not is_in_string:
        is_in_string = True
        is_string = True
        is_variable_name = False
        quotation_mark = char
      else:
        if char == quotation_mark and previous_char != "\\":
          is_in_string = False
    
    # If the current character is not part of a string, then skip or add the value to the list
    if not is_in_string:
      if char == " ":
        continue
      if char == ",":
        can_add_to_list = True
    
    if can_add_to_list:
      if is_string:
        # Checks if the value is a valid string type
        if inter_data_type(value) != "string":
          print("Error: Mismatched quotation mark")
          print_line(line_numb, line_list)
          return False
        
        first_quotation_mark = -1
        second_quotation_mark = -1
        
        # Need to add space because of indexing going out of bounds for
        # statements like *Display x, "' x '", y*
        value = value + " "
        
        # Finding the positions where the first and last quotation marks are
        for i in range(0, len(value)):
          if value[i] == quotation_mark and first_quotation_mark < 0:
            first_quotation_mark = i
          if value[len(value) - 1 - i] == quotation_mark and second_quotation_mark < 0:
            second_quotation_mark = len(value) - 1 - i
              
        # Checking if the quotation marks are the same.
        # They should be...
        if value[first_quotation_mark] == value[second_quotation_mark]:
          value_list.append({"data_type": "string", "value": value[first_quotation_mark:second_quotation_mark + 1]})
          
      if is_variable_name:
        if inter_data_type(value) == "number":
          value_list.append({"data_type": "number", "value": value})
        else:
          try:
            if all_variables[value] is not None:
              value_list.append({"data_type": "variable", "value": value})
          except:
            print("Error: Variable " + value + " has not been created.")
            print_line(line_numb, line_list)
            return False
          
      # Reset the value and make adding to the list false
      value = ""
      can_add_to_list = False
      is_in_string = False
      is_string = False
      is_variable_name = True
      continue
    
    # Build the value for each character
    value += char
    previous_char = char
  
  # Build the python line
  print_param = ""
  for data in value_list:
    if data["data_type"] == "string":
      print_param += data["value"] + " + "
    elif data["data_type"] == "variable" or data["data_type"] == "number":
      print_param += "str(" + data["value"] + ") + "
  print_param = print_param[0:-3]
  
  # Add the line to the list
  py_line = indent_space + "print(" + print_param + ")\n"
  py_lines.append(py_line)
  
  return True