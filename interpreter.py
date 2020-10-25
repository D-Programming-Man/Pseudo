import sys
from interlib import create
from interlib import display
from interlib import arithmetic

if __name__ == "__main__":
  # This file will later become a function to call, but for now let's just assume that this is the main function that takes in these files in the same directory
  in_file = open("test.pseudo", "r")
  py_file = open("outfile.py", "w")
  
  
  # All varaibles, list, and dictionaries are put into here from the "Create" keyword
  # Key = variable name, Values = {data type, data for that variable name}
  # For example, an entry in the dictionary could be {"x": {"data_type": "number", "value": 1}}
  # This means that x is a variable with the value 1
  # {}
  all_variables = {}
  
  # Line number where the parser is at, used for showing error exceptions.
  line_numb = 1

  # List of all python lines to be written to the outfile
  py_lines = []
  
  # Some initialization to write to the py_file
  py_lines.append('if __name__ == "__main__":\n')
  indent = 2
  parse_success = True
  
  # main loop to parse all words in the file
  for line in in_file:
  
    # If a line contains only whitespace, then we just add a newline
    # to keep the lines consistant with both the Pseudo code and the 
    # Python code
    if line.isspace():
      py_lines.append("\n")
      continue
      
    line_list = line.split(" ")
    
    # Filters out each line
    # Removes any newline characters if they are in the list
    try:
      while "\n" in line_list:
        line_list.remove("\n")
    except:
      pass
    
    # Removes any empty strings if they are in the list
    try:
      while '' in line_list:
        line_list.remove("")
    except:
      pass
        
    # Removes the newline character from teh last word 
    if line_list[-1][-1] == "\n":
      line_list[-1] = line_list[-1][:-1]
    
    # Checking each starting word to run their own handlers.
    # There should be something more optimal than doing elif statements.
    if line_list[0].lower() == "create":
      parse_success = create.handler(line_numb, line_list, py_lines, all_variables, indent, py_file)
    
    elif line_list[0].lower() == "add":
      parse_success = arithmetic.add(line_numb, line_list, py_lines, all_variables, indent, py_file)
    
    elif line_list[0].lower() == "subtract":
      parse_success = arithmetic.subtract(line_numb, line_list, py_lines, all_variables, indent, py_file)
    
    elif line_list[0].lower() == "multiply":
      parse_success = arithmetic.multiply(line_numb, line_list, py_lines, all_variables, indent, py_file)
    
    elif line_list[0].lower() == "divide":
      parse_success = arithmetic.divide(line_numb, line_list, py_lines, all_variables, indent, py_file)
    
    elif line_list[0].lower() == "display":
      parse_success = display.handler(line_numb, line_list, py_lines, all_variables, indent, py_file)
      
    # At the end of parsing the line, increment the line counter
    line_numb += 1
    
    # Terminate loop when error occurs
    if not parse_success:
      break

   # write every line into py_file
  for line in py_lines:
    py_file.write(line)
      
  # Debugging stuff
  #for var in all_variables:
  #  print(var + ": " + str(all_variables[var]))
  
  # Close the files 
  in_file.close()
  py_file.close()
  
  # Runs the output file, stores output into output.txt file
  default_stdout = sys.stdout
  output_file = open('output.txt', 'w')
  sys.stdout = output_file
  exec(open('outfile.py').read())
  output_file.close()
  sys.stdout = default_stdout
  
  # Print the output to the console
  out_file = open("output.txt", 'r')
  for line in out_file:
    print(line[0:-1])
  
  out_file.close()
