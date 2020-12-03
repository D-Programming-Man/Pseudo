from interlib.utility import inter_data_type
from interlib.utility import print_line


def handler(interpret_state):
  line_numb = interpret_state["line_numb"]
  line_list = interpret_state["line_list"]
  all_variables = interpret_state["all_variables"]
  indent = interpret_state["indent"] + interpret_state["pseudo_indent"]
  py_lines = interpret_state["py_lines"]

  update_statement = line_list.copy()
  update_statement.pop(0) # Remove keyword
  data_input = None
  data_key = None
  store_variable = None
  found_with = False

  for i in range(len(update_statement)):
    word = update_statement[i]

    if store_variable == None:
      store_variable  = word

    elif found_with == False:
      if word == "with":
        found_with = True

    elif data_key == None:
      first_char = word[0]
      last_char = word[-1]

      if first_char != "{":
        print("Error on line " + str(line_numb) + ". Bad syntax for Update.")
        print_line(line_numb, line_list)
        return False
      elif last_char != ":":
        print("Error on line " + str(line_numb) + ". Bad syntax for Update. Colon has to be right behind key then a space.")
        print_line(line_numb, line_list)
        return False
      else:
        data_key = word[1 : -1]
    
    elif data_input == None:
      last_char = word[-1]

      if last_char != "}":
        print("Error on line " + str(line_numb) + ". Bad syntax for Update.")
        print_line(line_numb, line_list)
        return False
      else:
        data_input = word[: -1]

  if store_variable == None or data_input == None or data_key == None or found_with == False:
    print("Error on line " + str(line_numb) + ". Bad syntax for Update.")
    print_line(line_numb, line_list)
    return False

  #Write update statement as python code
  indent_space = indent * " "
  py_line = indent_space + store_variable + "[" + data_key + "] = " + data_input + "\n"
  py_lines.append(py_line)

  store_table = all_variables.get(store_variable)

  if store_table == None:
    print("Error on line " + str(line_numb) + ". Not a table.")
    print_line(line_numb, line_list)
    return False

  if store_table["data_type"] != "table":
    print("Error on line " + str(line_numb) + ". Not a table.")
    print_line(line_numb, line_list)
    return False

  return True
