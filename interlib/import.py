from interlib.utility import print_line
from interlib.utility import import_interpret
import os
import sys
import glob

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
  
  if len(line_list) > 2:
    print("Cannot import files with spaces in the names.")
    print_line(line_numb, line_list)
    return False

  # Find the file in the same directory as the main pseudo file
  word_pos = 1
  file_list_pos = 0
  pseudo_files = glob.glob("./*.pseudo")
  for file in pseudo_files:
    file = file[2:-7]
    if file == line_list[1]:
      break;
    file_list_pos += 1

  pseduo_file_name = ""
  pseduo_file = ""
  pseduo_file_py = ""
  try:
    pseudo_file_name = pseudo_files[file_list_pos][2:-7]
    pseudo_file = pseudo_files[file_list_pos][2:]
    pseudo_file_py = pseudo_file_name + ".py"
  except:
    print("There is no pseudo file named \"" + line_list[1] + "\"")
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
  sub_interpret_state = import_interpret(pseudo_file, pseudo_file_py, interpret_state["keyword_dict"], import_queue)
  if sub_interpret_state["success"]:
    import_queue.pop()
    import_statement = "import " + pseudo_file_name +"\n" 
    py_lines.appendleft(import_statement)
    
    # Add all functions from the sub_interpret_state to the current interpret_state
    # error out if we override functions, print out what file name of where the
    # overriding function is at
    
  return sub_interpret_state["success"]
