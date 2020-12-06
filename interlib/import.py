from interlib.utility import print_line
from interlib.utility import import_interpret
import os
import sys
import glob

help_manual = "  Syntax: \n" \
              "  Import <pseudo file name> \n" \
              "  - The <pseudo file name> is a file name without the extension\n" \
              "  \n" \
              "  Examples: \n" \
              "  Import helper \n" \
              "  Import Some_Other_Pseudo_File \n" \
              "  Import Another_File \n"

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
 
 Eample: Import helper1
'''
def handler(interpret_state):
  line_numb = interpret_state["line_numb"]
  line_list = interpret_state["line_list"]
  all_variables = interpret_state["all_variables"]
  indent = interpret_state["pseudo_indent"] + interpret_state["indent"]
  py_lines = interpret_state["py_lines"]
  import_queue = interpret_state["import_queue"]
  pseudo_filepath = interpret_state["pseudo_filepath"]
  pseudo_file = interpret_state["pseudo_file"]
  
  if len(line_list) > 2:
    print("Cannot import files with spaces in the names.")
    print_line(line_numb, line_list)
    return False

  # Find the file in the same directory as the main pseudo file
  word_pos = 1
  file_list_pos = 0
  pseudo_files = glob.glob(pseudo_filepath + "/*.pseudo")
  #print(pseudo_files)
  for file in pseudo_files:
    file = file.split("\\")[-1][0:-7]
    #file = file[2:-7]
    #print(file)
    if file == line_list[1]:
      break;
    file_list_pos += 1

  pseudo_file_name = ""
  pseudo_filepath = ""
  pseudo_file_py = ""
  try:
    pseudo_file_name = pseudo_files[file_list_pos].split("\\")[-1]
    pseudo_filepath = pseudo_files[file_list_pos]
    pseudo_file_py = pseudo_files[file_list_pos][0:-7] + ".py"
  except:
    print("Error: There is no pseudo file named \"" + line_list[1] + ".pseudo\" within the same directory as \"" + pseudo_file + "\"")
    print_line(line_numb, line_list)
    return False

  # Check if the importing pseudo file is a queue of already imported files 
  if pseudo_file_name not in import_queue.queue:
    import_queue.push(pseudo_file_name)
  else:
    import_queue.remove(pseudo_file_name)
    import_queue.insert(import_queue.size(), pseudo_file_name)

  # Checks for infinite import loops
  if import_queue.is_infinite_loop():
    print("Error: Infinite loop of imports")
    return False

  # Parse all code in the importing pseudo file
  sub_interpret_state = import_interpret(pseudo_filepath, pseudo_file_py, interpret_state["keyword_dict"], import_queue)
  if sub_interpret_state["parse_success"]:
    import_queue.pop()
    
    # Add all functions from the sub_interpret_state to the current interpret_state
    # error out if we override functions, print out what file name of where the
    # overriding function is at
    contains_functions = False
    for var in sub_interpret_state["all_variables"]:
      if sub_interpret_state["all_variables"][var]["data_type"] == "function":
        if var not in all_variables:
          if sub_interpret_state["all_variables"][var]["source"] != pseudo_file:
            contains_functions = True
            interpret_state["all_variables"][var] = sub_interpret_state["all_variables"][var]
            py_lines.appendleft("from " + pseudo_file_name + " import " + var + "\n")
        else:
          print("Error: Function " + var + " is already defined in this file as well as in \"" + pseudo_file + "\".")
          return False
    if not contains_functions:
      py_lines.appendleft("import " + pseudo_file_name + "\n")
      
  return sub_interpret_state["parse_success"]
