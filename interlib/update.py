from interlib.utility import inter_data_type
from interlib.utility import print_line

help_manual = "  Note: \n" \
              "  - Only updates a table with one value at a time. \n" \
              "  - The spaces after the colon (:) is required. \n" \
              "  \n" \
              "  Syntax: \n" \
              "  Update <table> with {<datatype>: <datatype>} \n" \
              "  \n" \
              "  Examples: \n" \
              "  Update a_table with {\"Some\": \"Value\"} \n" \
              "  Update another_table with {1: \"1\"} \n" \
              "  Update name_table with {name_variable: value_variable} \n"

def handler(interpret_state):
  line_numb = interpret_state["line_numb"]
  line_list = interpret_state["line_list"]
  all_variables = interpret_state["all_variables"]
  indent = interpret_state["indent"] + interpret_state["pseudo_indent"]
  py_lines = interpret_state["py_lines"]

  update_statement = line_list.copy()
  update_statement.pop(0) # Remove keyword
  update_statement = syntax_parse(update_statement)

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

      if first_char != "{" or last_char != "}":
        print("Error on line " + str(line_numb) + ". Bad syntax for Update.")
        print_line(line_numb, line_list)
        return False
      
      word_split = word.split(':')
      if len(word_split) == 2:
        data_key = word_split[0][1:].strip()
        data_input = word_split[1][:-1].strip()
      else:
        print("Error on line " + str(line_numb) + ". Bad syntax for Update.")
        print_line(line_numb, line_list)
        return False

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

def syntax_parse(update_line):
  new_statement = ["", "", ""]
  for x in range(len(update_line)):
    if x < 2:
      new_statement[x] = update_line[x]
    else:
      new_statement[2] += update_line[x]
      if x != len(update_line)-1:
        new_statement[2] += " "

  return new_statement