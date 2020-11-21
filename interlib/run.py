from interlib.utility import print_line

'''
    Handler that allows running of functions

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

  word_pos = 2
  indent_space = indent * " "

  func_name = line_list[word_pos]

  if func_name not in all_variables:
    print("Error on line " + str(line_numb) + ". Must run an existing function.")
    print_line(line_numb, line_list)
    return False

  param_names = []

  if len(line_list) >= 4:
    word_pos += 1

    if line_list[word_pos] == "with":
      word_pos += 1
    else:
      print("Error on line " + str(line_numb) + ". Improper function running format.")
      print_line(line_numb, line_list)
      return False

    if line_list[word_pos] == "parameter" or line_list[word_pos] == "parameters":
      word_pos += 1
    else:
      print("Error on line " + str(line_numb) + ". Improper function running format.")
      print_line(line_numb, line_list)
      return False

    data_types = {"number": "int", "string": "str", "list": "list", "table": "dict"}

    while len(line_list) > word_pos:

      if line_list[word_pos] in data_types:
        word_pos += 1
      else:
        print("Error on line " + str(line_numb) + ". Improper data type.")
        print_line(line_numb, line_list)
        return False

      if line_list[word_pos][-1] == ",":
        param_names.append(line_list[word_pos] + " ")
      else:
        param_names.append(line_list[word_pos])
      word_pos += 1

  py_line = indent_space + func_name + "("

  i = 0

  for name in param_names:
    py_line += name

  py_line += ")\n"

  py_lines.append(py_line)

  return True
