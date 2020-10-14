# Used for printing out the line that is associated with the error message
# For line_numb, pass in the 
def print_line(lines_to_write, line_list):
  line = ""
  for word in line_list:
    line += word + " "
  print("Line " + str(len(lines_to_write)) + ': ' + line)
  
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
  pass
  
def subtract(line_numb, line_list, py_lines, all_variables, indent, py_file):
  pass
  
def multiply(line_numb, line_list, py_lines, all_variables, indent, py_file):
  pass

def divide(line_numb, line_list, py_lines, all_variables, indent, py_file):
  pass