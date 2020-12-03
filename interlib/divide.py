from interlib.utility import inter_data_type
from interlib.utility import print_line

'''
    Main arithmetic functions
    
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

  #length check: prevents access errors
  if(len(line_list)<7):
    print("Error on line " + str(line_numb) + ". Missing arguments, refer to divide usage.")
    print_line(line_numb, line_list)
    return False 

  var1 = line_list[1]
  var2 = line_list[3]
  offset = 0 
  #comma check: Spec requires comma
  if(var2[-1] !=','):
    print("Error on line " + str(line_numb) + ". Missing comma, refer to divide usage.")
    print_line(line_numb, line_list)
    return False
  var2 = var2[:-1]

  #error check: makes sure var1 exists or is a number
  if(inter_data_type(var1)!="number" and all_variables.get(var1)==None):
    print("Error on line " + str(line_numb) + ". Create "+var1+" before using divide")
    print_line(line_numb, line_list)
    return False   
  #format check: maintains Pseudo format
  if(line_list[2] != "by"):
    print("Error on line " + str(line_numb) + ". Expected \"by\" after first input")
    print_line(line_numb, line_list)
    return False
  #error check: makes sure var2 exists or is a number
  if(inter_data_type(var2)!="number" and all_variables.get(var2)==None):
    print("Error on line " + str(line_numb) + ". Create "+var2+" before using divide")
    print_line(line_numb, line_list)
    return False   

  #initialize values for var1 and var2, to be used in finding value
  var1_value = all_variables.get(var1)
  if(var1_value == None):
    if(var1.isdigit()):
       var1_value = int(var1)
    else:
      var1_value = float(var1)
  else:
    var1_value = all_variables[var1]["value"]

  # Problems will arise when the value loaded is 0
  # Problems will also arise when the Divdie is used in a funciton that uses an
  # uninitialized variable, which assuems that variable to be 0. So for this case,
  # we won't write the true value into the all_variables dictionary since we only
  # care about the data type.
  var2_value = all_variables.get(var2)
  if(var2_value == None):
    if(var2.isdigit()):
       var2_value = int(var2)
    else:
      var2_value = float(var2)
  else:
    var2_value = 1 #

  #format check: maintains Pseudo format
  if(line_list[4]!="store"):
    print("Error on line " + str(line_numb) + ". Expected \"store\" after second input")
    print_line(line_numb, line_list)
    return False
  #format check: maintains Pseudo format. updates offset
  if(line_list[5]=="it"):
    offset=1
  elif(line_list[5]=="the"):
    if(line_list[6]=="result"):
      offset = 2
    else:
      print("Error on line " + str(line_numb) + ". Expected \"result\" after \"the\" ")
      print_line(line_numb, line_list)
      return False
  #length check: prevents access errors, updated now that offset is known
  if(len(line_list)<7+offset):
    print("Error on line " + str(line_numb) + ". Missing arguments, refer to divide usage.")
    print_line(line_numb, line_list)
    return False  
  #format check: maintains Pseudo format
  if(line_list[5+offset]!="into"):
    print("Error on line " + str(line_numb) + ". Expected \"into\" before destination variable")
    print_line(line_numb, line_list)
    return False

  var3 = line_list[6+offset]
  if var2_value == 0:
    print("Error: Trying to divide by zero.")
    print_line(line_numb, line_list)
    return False
  
  if(inter_data_type(var3)!="number"):
    all_variables[var3] = {"data_type":"number","value":var1_value/var2_value}
  else:
    print("Error on line " + str(line_numb) + ". Expected "+var3+" to be a variable name")
    print_line(line_numb, line_list)
    return False      
  
  py_line = indent*" " + var3 + " = " + var1 + "/" + var2 +"\n"
  py_lines.append(py_line)
  return True
