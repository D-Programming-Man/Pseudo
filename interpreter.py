import sys
from interlib import create
#from interlib import display
#from interlib import arithmetic

if __name__ == "__main__":
  # This file will later become a function to call, but for now let's just assume that this is the main function that takes in these files in the same directory
  in_file = open("test.pseudo", "r")
  py_file = open("outfile.py", "w")
  
  
  # All varaibles, list, and dictionaries are put into here from the "Create" keyword
  # Key = variable name, Values = {data type, data for that variable name}
  # For example, an entry in the dictionary could be {"x": {"data_type": "variable", "value": 1}}
  # This means that x is a variable with the value 1
  # {}
  all_variables = {}
  
  # Line number where the parser is at, used for showing error exceptions.
  line_numb = 1
  
  # Some initialization to write to the py_file
  py_file.write('if __name__ == "__main__":\n')
  indent = 2
  parse_success = True
  
  # main loop to parse all words in the file
  for line in in_file:
    line_list = line.split(" ")
    if line_list[0].lower() == "create":
      parse_success = create.handler(line_numb, line_list, all_variables, indent, py_file)
    line_numb += 1
    
    if not parse_success:
      break
      
  # Debugging stuff
  for var in all_variables:
    print(var + ": " + str(all_variables[var]))
  
  # Close the files 
  in_file.close()
  py_file.close()