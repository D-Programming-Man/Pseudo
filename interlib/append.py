from interlib.utility import inter_data_type
from interlib.utility import print_line

help_manual = "  Syntax: \n" \
              "  Append (<datatype>) to <list> \n" \
              "  \n" \
              "  Examples: \n" \
              "  Append 1 to some_list \n" \
              "  Append x to another_list \n" \
              "  Append 1.234 to this_list \n" \
              "  Append [1,2,3] to some_list \n" \
              "  Append {1:\"SomeText\"} to table_list\n"

def handler(interpret_state):
  line_numb = interpret_state["line_numb"]
  line_list = interpret_state["line_list"]
  all_variables = interpret_state["all_variables"]
  indent = interpret_state["indent"] + interpret_state["pseudo_indent"]
  py_lines = interpret_state["py_lines"]

  append_statement = line_list.copy()
  append_statement.pop(0) # Remove keyword
  data_input = None
  store_variable = None
  found_to = False

  for i in range(len(append_statement)):
    word = append_statement[i]

    if data_input == None:
      data_input  = word

    elif found_to == False:
      if word == "to":
        found_to = True

    elif store_variable == None:
      store_variable = word

  if store_variable == None or data_input == None or found_to == False:
    print("Error on line " + str(line_numb) + ". Bad syntax for Append.")
    print_line(line_numb, line_list)
    return False

  #Write append statement as python code
  indent_space = indent * " "
  py_line = indent_space + store_variable + ".append(" + data_input + ")\n"
  py_lines.append(py_line)

  store_list = all_variables.get(store_variable)

  if store_list == None:
    print("Error on line " + str(line_numb) + ". Not a list.")
    print_line(line_numb, line_list)
    return False

  if store_list["data_type"] != "list":
    print("Error on line " + str(line_numb) + ". Not a list.")
    print_line(line_numb, line_list)
    return False

  return True