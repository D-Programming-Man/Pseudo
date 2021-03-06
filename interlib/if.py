from interlib.utility import inter_data_type
from interlib.utility import print_line

help_manual = "  Syntax: \n" \
              "  If (<variable>/<number>/<string>) is ([not] equal to/(less/greater) than [or equal to]) (<variable>/<number>/<string>): \n" \
              "     ... code goes here ... \n" \
              "  \n" \
              "  Examples: \n" \
              "  If 1 is not equal to 2: \n" \
              "    Display \"1 is not equal to 2, what did you expect?\" \n" \
              "  If x is less than 10: \n" \
              "    Add x and 10, store into x \n" \
              "    Display x \n" \
              "  If some_variable is greater than or equal to another_variable: \n" \
              "    Display \"Then do something with that variable in here\" \n" \
              "  If \"ThisString\" is equal to \"ThisString\": \n" \
              "    Display \"This only works for string that do not have spaces\" \n" \
              "  If \"ThisString\" is not equal to \"ThatString\": \n" \
              "    Add 1 and 1, store into result \n" \
              "    Display result \n"

'''
    Conditional Branch function
    If (<variable>/<number>/<string>) is [equal to/not equal to/less than [or equal to]/greater than [or equal to]] (<variable>/<number>/<string>):
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

  #check line size to make sure we aren't missing words 
  #5 is the min number of words to write an if statement ex: if var1 
  min_line_length = 6
  if(len(line_list) < min_line_length):
    print("Error on line " + str(line_numb) + ". Missing arguments, refer to if usage.")
    print_line(line_numb, line_list)
    return False

  #get variable 1 and check that it is valid
  var1_name = line_list[1]
  var1_datatype = inter_data_type(var1_name)
  #print (var1_datatype)
  if all_variables.get(var1_name) == None and var1_datatype != "number" and var1_datatype != "string":
    print("Error on line " + str(line_numb) + " Variable named " + var1_name + " is not defined.")
    print_line(line_numb, line_list)
    return False
  #check format
  if line_list[2] != "is":
    print("Error on line " + str(line_numb) + "Incorrect If syntax. Check usage.")
    print_line(line_numb, line_list)
    return False

  # as the expressions vary in length, buffer helps positioning
  buffer = 0
  # parse boolean expression
  bool_expresion = ""
  if line_list[3] == "equal" and line_list[4] == "to":
    if(len(line_list) < buffer + min_line_length):
      print("Error on line " + str(line_numb) + ". Missing arguments, refer to if usage.")
      print_line(line_numb, line_list)
      return False
    bool_expresion = "=="

  elif line_list[3] == "not": 
    buffer = 1
    if(len(line_list) < buffer + min_line_length):
      print("Error on line " + str(line_numb) + ". Missing arguments, refer to if usage.")
      print_line(line_numb, line_list)
      return False
    if(line_list[4]!="equal" and line_list[5]!="to"):
      print("Error on line " + str(line_numb) + ". Incomplete boolean expression. Do you mean: \"not equal to\"?")
      print_line(line_numb, line_list)
      return False
    bool_expresion = "!="

  elif line_list[3] == "less":
    if(line_list[4] != "than"):
      print("Error on line " + str(line_numb) + ". Incomplete boolean expression. Do you mean: \"less than\"?")
      print_line(line_numb, line_list)
      return False
    bool_expresion = "<"
    if(line_list[5]=="or"):
      if(len(line_list) != min_line_length + buffer):
        buffer = 3
        if(len(line_list) < buffer + min_line_length):
          print("Error on line " + str(line_numb) + ". Missing arguments, refer to if usage.")
          print_line(line_numb, line_list)
          return False
        if(line_list[6] != "equal" or line_list[7] != "to"):
          print("Error on line " + str(line_numb) + ". Incomplete boolean expression.Do you mean \"less than or equal to\"?")
          print_line(line_numb, line_list)
          return False
        bool_expresion = "<="

  elif line_list[3] == "greater":
    if(line_list[4] != "than"):
      print("Error on line " + str(line_numb) + ". Incomplete boolean expression. Do you mean: \"greater than\"?")
      print_line(line_numb, line_list)
      return False
    bool_expresion = ">"
    if(line_list[5]=="or"):
      if(len(line_list) != buffer + min_line_length):
        buffer = 3
        if(len(line_list) < buffer + min_line_length):
          print("Error on line " + str(line_numb) + ". Missing arguments, refer to if usage.")
          print_line(line_numb, line_list)
          return False
        if(line_list[6] != "equal" or line_list[7] != "to"):
          print("Error on line " + str(line_numb) + ". Incomplete boolean expression.Do you mean \"greater than or equal to\"?")
          print_line(line_numb, line_list)
          return False
        bool_expresion = ">="
  else:
    print("Error on line " + str(line_numb) + ". Incomplete boolean expression.")
    print_line(line_numb, line_list)
    return False 
    
  #check var2_name
  var2_name = line_list[5+buffer][:-1]
  var2_datatype = inter_data_type(var2_name)
  if all_variables.get(var2_name) == None and var2_datatype != "number" and var2_datatype != "string":
    print("Error on line " + str(line_numb) + ". Variable named " + var2_name + " is not defined.")
    print_line(line_numb, line_list)
    return False

  #check that both data types are the same
  var1_datatype = all_variables.get(var1_name).get("data_type") if var1_datatype=="null" else var1_datatype
  var2_datatype = all_variables.get(var2_name).get("data_type") if var2_datatype=="null" else var2_datatype
  if (var1_datatype != var2_datatype):
    print("Error on line " + str(line_numb)+": "+var1_name+":"+var1_datatype+" and "+var2_name+":"+var2_datatype+" are not the same data type.")
    print_line(line_numb, line_list)
    return False

  py_line = indent*" " + "if " + var1_name + bool_expresion + var2_name +":\n"
  py_lines.append(py_line)
  return True