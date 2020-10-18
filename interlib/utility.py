
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

# Returns the string "null" to indicate an unknown data type
def null_data_type(data):
  # Debug stuff
  #print("Unknown data type passed")
  #print("Function: inter_data_type(" + data + ")")
  return "null"

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
  for char in data:
    if not char.isdigit():
      if char == '.' and not encounter_period:
        encounter_period = True
      else:
        return null_data_type(data)
  
  # If it passes the number check, then it must be a number  
  return "number"
