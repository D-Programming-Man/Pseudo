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
  indent = interpret_state["indent"]
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

  var2_value = all_variables.get(var2)
  if(var2_value == None):
    if(var2.isdigit()):
       var2_value = int(var2)
    else:
      var2_value = float(var2)
  else:
    var2_value = all_variables[var2]["value"]

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
  if(inter_data_type(var3)!="number"):
    all_variables[var3] = {"data_type":"number","value":var1_value/var2_value}
  else:
    print("Error on line " + str(line_numb) + ". Expected "+var3+" to be a variable name")
    print_line(line_numb, line_list)
    return False      
  
  py_line = indent*" " + var3 + " = " + var1 + "/" + var2 +"\n"
  py_lines.append(py_line)
  return True




# Helper functions I(Dvir) use, final version might not need these
def is_valid_number(element):
  # Will either return the string as an integer or float, both valid, or return None
  if element.isnumeric():
    return int(element)
  try:
    float(element)
    return float(element)
  except:
   pass


def data_type_check(name, all_variables):
  # if it exists, returns data type
  # else None
  if name in all_variables:
    return all_variables[name]["data_type"]
  else:
    pass

#Helper function for Multiply
#Checks if var is a number or a variable in all_varaibles
#This is called for places where var is allowed to be a variable or a number
def variableCheck(var, all_variables): 
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