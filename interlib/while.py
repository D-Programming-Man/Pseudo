from interlib.utility import inter_data_type
from interlib.utility import print_line


def handler(interpret_state):
  line_numb = interpret_state["line_numb"]
  line_list = interpret_state["line_list"]
  all_variables = interpret_state["all_variables"]
  indent = interpret_state["indent"]
  py_lines = interpret_state["py_lines"]

  while_statement = line_list
  while_statement.pop(0) # Remove while word
  operand1 = None
  operand2 = None
  operation = ""
  found_is = False

  for i in range(len(while_statement)):
    word = while_statement[i]

    #Last word is assumed to be the second operand with a colon
    if i == len(while_statement) - 1:
      last_char = word[-1]
      if last_char == ":":
        operand2 = word[:-1]
      else:
        print("Error, incorrect syntax for while") # Missing colon at end
        print_line(line_numb, line_list) 
        return False

    #operand1 should be the first thing initialized (word after while)
    elif operand1 == None:
      operand1 = word

    #We want to make sure the "is" word is always present
    elif found_is == False:
      if word == "is":
        found_is = True

    # Every word not part of the operands or "is" is part of the operation
    else:
      operation = operation + " " + word

  if operand1 == None or operand2 == None or operation == "" or found_is == False:
    print("Error, incorrect syntax for while") # Missing colon at end
    print_line(line_numb, line_list)
    return False

  #Write while statement as python code
  indent_space = indent * " "
  operation_py = operation_interpreter(operation)
  if operation_py == None:
    print("Error, incorrect syntax for while") # Missworded condition
    print_line(line_numb, line_list)
    return False
  py_line = indent_space + "while " + operand1 + " " + operation_py + " " +  operand2 + ":\n"
  py_lines.append(py_line)
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