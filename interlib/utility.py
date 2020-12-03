import sys
import os
from collections import deque

# A small class used for the Import keyword to keep track of
# cyclic imports of other .pseudo files
class ImportQueue():
  def __init__(self):
    self.queue = []
    self.queue_rotation = 0
    self.MAX_ROTATION = 20
        
  def is_infinite_loop(self):
    return self.queue_rotation > self.MAX_ROTATION

  def size(self):
    return len(self.queue)

  def insert(self, pos, data):
    self.queue.insert(pos, data)
    self.queue_rotation += 1
    
  def remove(self, data):
    self.queue.remove(data)
    
  def push(self, data):
    self.queue.append(data)
  
  def pop(self):
    temp = self.queue.pop()
    self.queue_rotation = 0
    return temp

# Returns the string "null" to indicate an unknown data type
def null_data_type(data):
  # Debug stuff
  #print("Unknown data type passed")
  #print("Function: inter_data_type(" + data + ")")
  return "null"

'''
    Figures out the data type of what it is given.

Requires:
 . data = A string
 
Returns:
 . A string that describes the data. All returns only have these values:
   - "number"   (Can be either an integer or a float)
   - "string"
   - "list"
   - "table"
   - "function" NOT YET IMPLEMENTED
   - "object"   NOT YET IMPLEMENTED
   - "null"  (Not a valid data type)
'''
def inter_data_type(data):
  char_pos = 0
  return_data_type = ""
  
  # If we detect qutation marks at the beginning of the data, then it could be a string
  if data[char_pos] == "'" or data[char_pos] == '"':
    first_quote_pos = 0
    second_quote_pos = 0
    quotation_mark = data[char_pos]
    data_len = len(data)
    previous_char = ""
    
    # Check where the second qutation mark is at in the data
    for i in range(0, len(data)):
      if data[data_len - 1 - i] == quotation_mark:
        second_quote_pos = data_len - 1 - i
        break;
    
    # This means that there's only 1 quotation mark in the data
    if first_quote_pos == second_quote_pos:
      return null_data_type(data)
      
    # Check through the string to see if there is the same quotation_mark value within it.
    for i in range(first_quote_pos + 1, second_quote_pos):
      if data[i] == quotation_mark and previous_char != "\\":
        return null_data_type(data)
      previous_char = data[i]
    
    # If the data value passed all of these test, then it must be a string
    return "string"
  
  # Could be a list if we encounter a bracket
  if data[char_pos] == "[":
    pass
    
  # Could be a table if we encounter a brace
  if data[char_pos] == "{":
    pass
    
  # Knowing that it is not any of these, then it could be a number
  encounter_period = False
  for char in range(0, len(data)):
    if not data[char].isdigit():
      if data[char] == '.' and not encounter_period:
        encounter_period = True
      elif data[char] == '-' and char == 0:
        continue
      else:
        return null_data_type(data)
        
  # If it passes the number check, then it must be a number  
  return "number"

import keyword

def key_var_check(var_dict, value_list):
  for value in value_list:
    val_type = inter_data_type(value)
    if val_type == "null":
      if keyword.iskeyword(value):
        return None
      if value not in var_dict:
        return None

  return True
  
# Used for printing out the line that is associated with the error message
def print_line(line_numb, line_list):
  line = ""
  for word in line_list:
    line += word + " "
  print("Line " + str(line_numb + 1) + ': ' + line)

# Used within the "Import" handler to translate the other pseudo files into python files.
# Similar to the interpret function, but slightly modifed
def import_interpret(pseudo_file, python_file, keyword_dict, import_queue):
  in_file = open(pseudo_file, "r")
  py_file = open(python_file, "w")
  
  if (os.stat(pseudo_file).st_size == 0):
    print("Error: Pseudo file " + pseduo_file + " emtpy. Did you properly saved it first?")
    err = {"success": False}
    return err
    
  in_file_lines = []
  for line in in_file:
    in_file_lines.append(line)

  all_variables = {}
  line_numb = 0
  py_lines = deque()
  indent = 0
  parse_success = False

  interpret_state = {}
  interpret_state["all_variables"] = all_variables
  interpret_state["line_numb"] = line_numb
  interpret_state["py_lines"] = py_lines
  interpret_state["indent"] = indent
  interpret_state["parse_success"] = parse_success
  interpret_state["in_file_lines"] = in_file_lines
  interpret_state["keyword_dict"] = keyword_dict
  interpret_state["import_queue"] = import_queue
  interpret_state["pseudo_file"] = pseudo_file

  while interpret_state["line_numb"] < len(in_file_lines):
    curr_pc = interpret_state["line_numb"]
    line = in_file_lines[interpret_state["line_numb"]]

    if line.isspace():
      py_lines.append("\n")
      interpret_state["line_numb"] = interpret_state["line_numb"] + 1
      continue

    pseudo_indent = 0
    for char in line:
      if char != " ":
        break
      pseudo_indent += 1
    interpret_state["pseudo_indent"] = pseudo_indent
  
    line_list = line.split(" ")

    while "\n" in line_list:
      line_list.remove("\n")

    while '' in line_list:
      line_list.remove("")

    if line_list[-1][-1] == "\n":
      line_list[-1] = line_list[-1][:-1]

    # Check if the very first character of the line is a #, Pycode, or % and if so then put the whole line into the py_lines list and parse the next line
    interpret_state["parse_success"] = True
    if line_list[0][0] == "#":
      py_lines.append((pseudo_indent + interpret_state["indent"]) * " " + line)
    elif line_list[0].lower() == "pycode" or line_list[0][0] == "%":
      py_line = ""
      if line_list[0][0] == "%" and len(line_list[0]) > 1:
        py_line += line_list[0][1:] + " "
      for i in range(1, len(line_list)):
        py_line += line_list[i] + " "
      py_lines.append((pseudo_indent+interpret_state["indent"])*" " + py_line + "\n")
    else:
      interpret_state["line_list"] = line_list
      keyword = line_list[0].lower()
      try:
        interpret_state["parse_success"] = keyword_dict[keyword].handler(interpret_state)
      except KeyError:
        print("Error: \"" + line_list[0] + "\" keyword not known in file " + pseudo_file +".")
        print_line(interpret_state["line_numb"], line_list)
        interpret_state["parse_success"] = False;
      except IndexError:
        print("Pseudo code line incomplete in file " + pseudo_file + ".")
        print_line(interpret_state["line_numb"], line_list)
        interpret_state["parse_success"] = False;

    if interpret_state["line_numb"] == curr_pc:
      interpret_state["line_numb"] += 1

    if not interpret_state["parse_success"]:
      in_file.close()
      py_file.close()
      return interpret_state
    
  for line in py_lines:
    py_file.write(line)
  
  in_file.close()
  py_file.close()
  
  return interpret_state

