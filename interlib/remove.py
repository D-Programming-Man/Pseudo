from interlib.utility import inter_data_type
from interlib.utility import print_line

'''
    List/Dictionary Modification Function
    Remove <datatype> from (<list>/<table>)    
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

  #length check: prevents access errors
  if(len(line_list)< 4):
    print("Error on line " + str(line_numb) + ". Missing arguments, refer to divide usage.")
    print_line(line_numb, line_list)
    return False 
  
  #check for format
  if(line_list[2] != "from"):
    print("Error on line " + str(line_numb) + ". Incorrect Remove syntax. Check usage.")
    print_line(line_numb, line_list)
    return False 

  # check list/dictionary exists
  container_name = line_list[3]
  container_datatype = all_variables.get(container_name)
  if(container_datatype==None and (container_datatype.get("data_type") == "list" or container_datatype == "table")):
    print("Error on line " + str(line_numb) + ". " + container_name + " is not of type list or table.")
    print_line(line_numb, line_list)
    return False
  container_datatype = container_datatype.get("data_type")
  
  #check to see if the element is a variable, if it is then check to see if it exists  
  element_name = line_list[1]
  if(inter_data_type(element_name) == "null" and all_variables.get(element_name)== None):
    print("Error on line " + str(line_numb) + ". " + element_name + " is not a valid type.")
    print_line(line_numb, line_list)
    return False 

  #list and dictionaries(tables) require different python functions
  py_line = ""
  if(container_datatype=="list"):
    py_line = indent*" " + container_name + ".remove(" + element_name + ")\n"
  else:
    py_line = indent*" " + "del " + container_name + "[" + element_name + "]\n"
  py_lines.append(py_line)
  return True