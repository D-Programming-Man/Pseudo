import sys
import os
from collections import deque
from interlib.utility import ImportQueue
from interlib.utility import print_line

def interpret(pseudo_file, python_file, keyword_dict):
  in_file = open(pseudo_file, "r")
  py_file = open(python_file, "w")
  default_stdout = sys.stdout
  output_file = open('output.txt', 'w')
  sys.stdout = output_file
  
  if (os.stat(pseudo_file).st_size == 0):
    print("Error: Pseudo file emtpy. Did you properly saved it first?")
    
  # Puts all of the lines from the input file to a list
  in_file_lines = []
  for line in in_file:
    in_file_lines.append(line)
    
  # All varaibles, list, and dictionaries are put into here from the "Create" keyword
  # Key = variable name, Values = {data type, data for that variable name}
  # For example, an entry in the dictionary could be {"x": {"data_type": "number", "value": 1}}
  # This means that x is a variable with the value 1
  all_variables = {}
  
  # Line number where the parser is at, used for showing error exceptions.
  line_numb = 0

  # List of all python lines to be written to the outfile
  py_lines = deque()
  
  # Some initialization to write to the py_file
  py_lines.appendleft('if __name__ == "__main__":\n')
  indent = 2
  parse_success = False
  
  # In the future, we might want to add our own values to pass to a function for specific cases. In order to generalize, we will put any important values into this dictionary and pass this dictionary around to all of the keyword functions
  # NOTE: dict and list are passed by reference
  # NOTE: numbers and strings are passed by value
  interpret_state = {}
  interpret_state["all_variables"] = all_variables
  interpret_state["line_numb"] = line_numb
  interpret_state["py_lines"] = py_lines
  interpret_state["indent"] = indent
  interpret_state["parse_success"] = parse_success
  interpret_state["in_file_lines"] = in_file_lines
  interpret_state["keyword_dict"] = keyword_dict
  interpret_state["pseudo_indent"] = 0
  interpret_state["import_queue"] = ImportQueue()
  interpret_state["pseudo_file"] = pseudo_file
  

  # main loop to parse all words in the file
  while interpret_state["line_numb"] < len(in_file_lines):
    curr_pc = interpret_state["line_numb"]
    line = in_file_lines[interpret_state["line_numb"]]

    # If a line contains only whitespace, then we just add a newline
    # to keep the lines consistant with both the Pseudo code and the 
    # Python code
    if line.isspace():
      py_lines.append("\n")
      interpret_state["line_numb"] = interpret_state["line_numb"] + 1
      continue
    
    # Checks how many spaces are at the beginning of the line
    pseudo_indent = 0
    for char in line:
      if char != " ":
        break
      pseudo_indent += 1
    interpret_state["pseudo_indent"] = pseudo_indent
  
    line_list = line.split(" ")
    
    # Filters out each line
    # Removes any newline characters if they are in the list
    while "\n" in line_list:
      line_list.remove("\n")
    
    # Removes any empty strings if they are in the list
    while '' in line_list:
      line_list.remove("")
        
    # Removes the newline character from the last word
    if line_list[-1][-1] == "\n":
      line_list[-1] = line_list[-1][:-1]
    
    # Check if the very first character of the line is a #, Pycode, or % and if so then put the whole line into the py_lines list and parse the next line
    interpret_state["parse_success"] = True
    if line_list[0][0] == "#":
      py_lines.append((pseudo_indent+interpret_state["indent"])*" " + line)
    elif line_list[0].lower() == "pycode" or line_list[0][0] == "%":
      py_line = ""
      if line_list[0][0] == "%" and len(line_list[0]) > 1:
        py_line += line_list[0][1:] + " "
      for i in range(1, len(line_list)):
        py_line += line_list[i] + " "
      py_lines.append((pseudo_indent+interpret_state["indent"])*" " + py_line + "\n")
    else:
      interpret_state["line_list"] = line_list
    
      # Parse the lines based on the keywords
      keyword = line_list[0].lower()
      try:
        interpret_state["parse_success"] = keyword_dict[keyword].handler(interpret_state)
      except KeyError:
        print("Error: \"" + line_list[0] + "\" keyword not known.")
        print_line(interpret_state["line_numb"], line_list)
        interpret_state["parse_success"] = False;
      except IndexError:
        print("Pseudo code line incomplete")
        print_line(interpret_state["line_numb"], line_list)
        interpret_state["parse_success"] = False;
      
    # At the end of parsing the line, increment the line counter
    # if we did not change the program counter
    if interpret_state["line_numb"] == curr_pc:
      interpret_state["line_numb"] += 1

    # Terminate loop when error occurs
    if not interpret_state["parse_success"]:
      return
      
  # write every line into py_file
  for line in py_lines:
    py_file.write(line)
      
  # Debugging stuff
  #for var in all_variables:
  #  print(var + ": " + str(all_variables[var]))
  
  # Close the files 
  in_file.close()
  py_file.close()
  
  # Runs the output file, stores output into output.txt file
  py_cmds = ""
  
  # Kind of stupid, but apparently the output.txt file will not
  # generate the outputs because of the if __name__ == "__main__"
  # line. So we need to omit this and then omit the two space
  # indentation for all lines after it.
  py_line_main_pos = py_lines.index('if __name__ == "__main__":\n')
  py_lines.remove('if __name__ == "__main__":\n')
  for i in range(0, len(py_lines)):
    if i < py_line_main_pos:
      py_cmds += py_lines[i]
    else:
      py_cmds += py_lines[i][2:]
  
  # Print the outputs to the output.txt file
  recursive_fix = {}
  try:
    exec(py_cmds, recursive_fix)
  except:
    print("Error: Something in your python code did not execute successfully.")
    print("       Check to make sure that your pseudo code is correctly formatted.")
  output_file.close()
  sys.stdout = default_stdout
  
  # Print the output to the console
  #out_file = open("output.txt", 'r')
  #for line in out_file:
  #  print(line[0:-1])
  
  #out_file.close()

