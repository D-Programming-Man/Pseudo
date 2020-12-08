from interlib.utility import inter_data_type
from interlib.utility import print_line

help_manual = "  Note: \n" \
              "  - You can only use a <number> for getting elements out of a list. That <number> \n" \
              "      is actually a position within the list to get from. \n" \
              "  - For tables, you can use any <variable>, <number>, or <string> value to get data \n" \
              "      out of it. \n" \
              "  - Your program will not run if the specified elements are not in the list. \n" \
              "  \n" \
              "  Syntax: \n" \
              "  Get (<variable>/<number>/<string>) from <list/table> and store [it] into <variable> \n" \
              "  \n" \
              "  Examples: \n" \
              "  Get 1 from number_list and store it into x \n" \
              "  Get \"Text\" from a_table and store into data \n" \
              "  Get 1 from another_table and store it into data \n" \
              "  Get x from new_table and store into result \n"

def handler(interpret_state):
  line_numb = interpret_state["line_numb"]
  line_list = interpret_state["line_list"]
  all_variables = interpret_state["all_variables"]
  indent = interpret_state["indent"] + interpret_state["pseudo_indent"]
  py_lines = interpret_state["py_lines"]

  get_statement = line_list.copy()
  get_statement.pop(0) # Remove keyword
  
  data_type = None
  input_table = None
  store_variable = None
  
  found_from = False
  found_store = False
  found_into = False

  for i in range(len(get_statement)):
    word = get_statement[i]

    if data_type == None:
      data_type  = word

    elif found_from == False:
      if word == "from":
        found_from = True

    elif input_table == None:
      input_table = word

    elif word == "and" or word == "it":
      continue

    elif found_store == False:
      if word == "store":
        found_store = True

    elif found_into == False:
      if word == "into":
        found_into = True

    elif store_variable == None:
      store_variable = word
      
  if data_type == None or input_table == None or store_variable == None:
    print("Error on line " + str(line_numb) + ". Bad syntax for Get.")
    print_line(line_numb, line_list)
    return False

  if found_from == False or found_store == False or found_into == False:
    print("Error on line " + str(line_numb) + ". Bad syntax for Get.")
    print_line(line_numb, line_list)
    return False

  table = all_variables.get(input_table)
  indent_space = indent * " "

  if table == None:
    print("Error on line " + str(line_numb) + ". Not a table or list.")
    print_line(line_numb, line_list)
    return False
  if table["data_type"] != "table" and table["data_type"] != "list":
    print("Error on line " + str(line_numb) + ". Not a table or list.")
    print_line(line_numb, line_list)
    return False

  py_line = indent_space + store_variable + " = "+ input_table + "[" + data_type + "]\n"
  py_lines.append(py_line)

  return True
