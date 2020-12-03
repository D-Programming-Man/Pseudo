from interlib.utility import print_line

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
  pseudo_file = interpret_state["pseudo_file"]

  word_pos = 2
  indent_space = indent * " "

  func_name = line_list[word_pos]
  if func_name[-1] == ":":
    func_name = func_name[0:-1]

  if func_name in all_variables:
    print("Error: The function name cannot be shared or overwritten.")
    print_line(line_numb, line_list)
    return False

  param_names = []
  param_types = []

  if len(line_list) >= 4:
    word_pos += 1

    if line_list[word_pos] == "with":
      word_pos += 1
    else:
      print("Error: Improper function declaration format.")
      print_line(line_numb, line_list)
      return False

    if line_list[word_pos] == "parameter" or line_list[word_pos] == "parameters":
      word_pos += 1
    else:
      print("Error: Improper function declaration format.")
      print_line(line_numb, line_list)
      return False

    data_types = {"number": "int", "string": "str", "list": "list", "table": "dict"}

    while len(line_list) > word_pos:

      datatype = line_list[word_pos]
      if datatype in data_types:
        param_types.append(data_types[datatype])
        word_pos += 1
      else:
        print("Error: Improper data type.")
        print_line(line_numb, line_list)
        return False

      var_name = line_list[word_pos]
      if var_name[-1] == "," or var_name[-1] == ":":
        param_names.append(var_name[:-1])
        all_variables[var_name[:-1]] = {"data_type": datatype, "value": 0}
      else:
        param_names.append(line_list[word_pos])
        all_variables[var_name] = {"data_type": datatype, "value": 0}


      word_pos += 1


  py_line = indent_space + "def " + func_name + "("

  i = 0
  param_dict = {}

  while i < len(param_names):
    py_line += param_names[i] + ": " + param_types[i]
    param_dict[param_names[i]] = param_types[i]
    i += 1
    if i < len(param_names):
      py_line += ", "

  py_line += "):\n"

  py_lines.append(py_line)

  all_variables[func_name] = {"data_type": "function", "value": param_dict, "source": pseudo_file}

  return True
