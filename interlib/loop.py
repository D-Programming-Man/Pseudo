from interlib.utility import print_line
from interlib.utility import inter_data_type
from interlib.utility import key_var_check

'''
    Handler that allows creation of functions

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

  word_pos = 1
  indent_space = indent * " "

  iterator_name = line_list[word_pos]
  iterator_value = None

  if(iterator_name.isdigit() == False and all_variables.get(iterator_name) == None):
    print("Error on line " + str(line_numb) + iterator_name +
          " is not a valid integer. Refer to looping documentation")
    print_line(line_numb, line_list)
    return False
  if(iterator_name.isdigit() == False):
    temp = all_variables.get(iterator_name)
    if(type(temp["value"]) is not int):
        print("Error on line " + str(line_numb) + iterator_name +
              " is not a valid integer. Refer to looping documentation")
        print_line(line_numb, line_list)
        return False
    else:
      iterator_name = str(temp["value"])
  else:
    #   it is a number, still check if its an integer?
    iterator_value = iterator_name
  # Checking the next word matches and if there is an optional phrase
  step_name = ""
  word_pos += 1
  step_size = None
  if line_list[word_pos] != "times" and line_list[word_pos] != "times:":
    print("Error on line " + str(line_numb) + ". Syntax error: Expected word 'times'")
    print_line(line_numb, line_list)
    return False
# Need to make sure I dont step bounds better than this
  if line_list[word_pos] == "times":  
    word_pos += 1
    if(line_list[word_pos] == "with" and line_list[word_pos+1] == "step"
    and line_list[word_pos+2] == "size" and line_list[word_pos+3] == "of"):
        step_name = line_list[word_pos+4]
        if step_name[-1:] == ":":
          step_name = step_name[:-1]

        if(step_name.isdigit() == False and all_variables.get(step_name) == None):
            print("Error on line " + str(line_numb) + step_name +
                " is not a valid integer. Refer to looping documentation")
            print_line(line_numb, line_list)
            return False

        if(step_name.isdigit() == False):
            temp = all_variables.get(step_name)
            if(type(temp["value"]) is not int):
                print("Error on line " + str(line_numb) + step_name +
                    " is not a valid integer. Refer to looping documentation")
                print_line(line_numb, line_list)
                return False
            else:
                # variable is an integer
                step_name = str(temp["value"])
        else:
            # it is a number, still check if its an integer?
            step_size = step_name

  py_line = indent_space + "for ahdfienf in range (0,"

  if iterator_value == None: 
    py_line += iterator_name
  else:
    py_line += iterator_value

  if step_size == None:
    py_line += ","+step_name
  else:
    py_line += ","+step_size

  py_line += "):\n"
  py_lines.append(py_line)

  return True
