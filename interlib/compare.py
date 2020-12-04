from interlib.utility import inter_data_type
from interlib.utility import print_line

help_manual = "  Syntax: \n" \
              "  Compare (<variable>/<number>/<string>) is ([not] equal to/(less/greater) than [or equal to]) (<variable>/<number>/<string>), store [it/the result] into <variable> \n" \
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

  compare_statement = line_list
  compare_statement.pop(0) # Remove compare keyword
  operand1 = None
  operand2 = None
  store_variable = None
  operation = ""
  found_is = False
  found_store = False

  for i in range(len(compare_statement)):
    word = compare_statement[i]

    #Last word is store variable
    if i == len(compare_statement) - 1:
      store_variable = word
    
    #operand2 should be the word before store
    elif compare_statement[i+1] == "store":
      lastChar = word[-1]
      if lastChar != ",":
        print("Error, missing comma")
        print_line(line_numb, line_list)
        return False
      else:
        operand2 = word[:-1]

    #operand1 should be the first thing initialized (word after compare)
    elif operand1 == None:
      operand1 = word

    #We want to make sure the "is" word is always present
    elif found_is == False:
      if word == "is":
        found_is = True

    # getting full operation sentence
    elif found_store == False:
      if word == "store":
        found_store = True
      else:
        operation = operation + " " + word

  if operand1 == None or operand2 == None or store_variable == None:
    print("Error, incorrect syntax for compare 1")
    print_line(line_numb, line_list)
    return False

  if operation == "" or found_is == False or found_store == False:
    print("Error, incorrect syntax for compare 2")
    print(operation)
    print_line(line_numb, line_list)
    return False

  #Write compare statement as python code
  indent_space = indent * " "
  operation_py = operation_interpreter(operation)
  if operation_py == None:
    print("Error, incorrect syntax for compare 3") # Missworded condition
    print_line(line_numb, line_list)
    return False
  py_line = indent_space + store_variable + " = " + operand1 + " " + operation_py + " " +  operand2 + "\n"
  py_lines.append(py_line)

  op1 = operand_get(operand1, all_variables)
  op2 = operand_get(operand2, all_variables)
  all_variables[store_variable] = {"data_type": "boolean", "value": operation_checker(op1, op2, operation)}
  return True

#Gets value from from an operand.
def operand_get(word, all_variables):
  op_type = inter_data_type(word)

  if op_type == "null" or op_type == "number":
    return variable_check(word, all_variables)

  elif op_type == "string":
    return word

#Gets value from from a conditional operation in psuedo.
def operation_checker(op1, op2, operation):
  if operation == " equal to":
    return op1 == op2
  elif operation == " not equal to":
    return op1 != op2
  elif operation == " less than":
    return op1 < op2
  elif operation == " greater than":
    return op1 > op2
  elif operation == " less than or equal to":
    return op1 > op2
  elif operation == " greater than or equal to":
    return op1 > op2
  else:
    #to throw error. Operation not valid
    return None

#Gets python version of conditional operation in psuedo.
def operation_interpreter(operation):
  if operation == " equal to":
    return "=="
  elif operation == " not equal to":
    return "!="
  elif operation == " less than":
    return "<"
  elif operation == " greater than":
    return ">"
  elif operation == " less than or equal to":
    return "<="
  elif operation == " greater than or equal to":
    return ">="
  else:
    #to throw error. Operation not valid
    return None

#Gets value from all_variables or
#returns the number of a string if it's a number in string form
def variable_check(var, all_variables): 
  if var.replace('.', '', 1).isdigit():
    if var.isdigit():
      return int(var)
    else:
      return float(var)
  else:
    temp = all_variables.get(var)
    if temp != None:
      if temp["data_type"] == "number":
        return temp["value"]
      else:
        return None
    else:
      return None
