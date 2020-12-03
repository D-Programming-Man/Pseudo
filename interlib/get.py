from interlib.utility import inter_data_type
from interlib.utility import print_line


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
  if table["data_type"] == "table":
    py_line = indent_space + store_variable + " = "+ input_table + "[" + data_type + "]\n"
  elif table["data_type"] == "list":
    #To change
    py_line = indent_space + store_variable + " = "+ input_table + "[" + data_type + "]\n"
  else:
    print("Error on line " + str(line_numb) + ". Not a table or list.")
    print_line(line_numb, line_list)
    return False

  py_lines.append(py_line)

  return True