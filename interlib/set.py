from interlib.utility import key_var_check
from interlib.utility import print_line
from interlib.utility import inter_data_type
from interlib.utility import list_dict_checker

help_manual = "  Syntax: \n" \
              "  Set <variable_name> [equal] to (<variable>/<number>/<string>/<list>/<table>) \n" \
              "  \n" \
              "  Examples: \n" \
              "  Set x to \"Hello World\" \n" \
              "  Set y equal to 1232 \n" \
              "  Set z to [1, 3 , 4, \"hmm\"] \n" \
              "  Set recipe to {\"Milk\" : \"2 lbs\", \"Crackers\" : \"Handful\"} \n"


'''
 Set keyword: used as a more advanced create option

 Requires:
 . line_numb = The line number we are looking at in the Psudo code file
 . line_list = The line we took from the Psudo code file, but in list format
 . all_variables = The dictionary that contains all of the variables for that Psudo code file
 . indent = The indentation to correctly format the line of python code
 . py_lines = The python code that we will append our finalized parsed code to it

 Returns:
 . A boolean value. This is used in the interpreter.py file to make sure that the parsing of the code executes correctly. Otherwise the parsing stops and ends it prematurely.

'''


def handler(interpret_state):
    line_numb = interpret_state["line_numb"]
    line_list = interpret_state["line_list"]
    all_variables = interpret_state["all_variables"]
    indent = interpret_state["pseudo_indent"] + interpret_state["indent"]
    py_lines = interpret_state["py_lines"]

    indent_space = indent * " "

    # The position of the line_list
    word_pos = 1

    var_name = line_list[word_pos]

    word_pos += 1


    while line_list[word_pos] != "to":
      word_pos += 1
    word_pos += 1

    if line_list[word_pos][0] == "[":
      value_list = line_list[word_pos:]
      if list_dict_checker("list", all_variables, value_list):
        value = " ".join(value_list)
        data_type = "list"
      else:
        print("Error: Invalid list")
        print_line(line_numb, line_list)
        return False
      
    elif line_list[word_pos][0] == "{":
      value_list = line_list[word_pos:]
      if list_dict_checker("table", all_variables, value_list):
        value = " ".join(value_list)
        data_type = "table"
      else:
        print("Error: Invalid table")
        print_line(line_numb, line_list)
        return False
      
    else:  

      value_list = line_list[word_pos:]
      value = " ".join(value_list)

      if key_var_check(all_variables, [value]) is None:
        print("Error on line " + str(line_numb+1) + ". " + var_name + " is being set to an invalid value.")
        print_line(line_numb, line_list)
        return False
        
      data_type = inter_data_type(value)

    py_line = indent_space + var_name + " = " + value + "\n"

    py_lines.append(py_line)

    all_variables[var_name] = {"data_type": data_type, "value": value}

    return True
