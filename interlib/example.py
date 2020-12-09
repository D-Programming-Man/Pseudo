from interlib.utility import print_line

'''
. This keyword file is an exmaple keyword that will show
you how you can implement your own keyword to Pseudo.
What you will need to know is the interpret_state's 
data, how to add to it before executing the interpretation
on the GUI/IDE, setting up the help_manual string, how
to write out python code to the output display (right screen
of the GUI/IDE), and successful parse your keyword by the
use of this file's handler() function

+-+-+-+- INTERPRET STATE -+-+-+-+:
. The interpret_state is a dictionary that contains all of the
important variables that make the interpretation successful.
. Here is a list of all of the keys in the interpret_state:

  - "all_variables":
    . This holds all of the interpreter's known variables and the datatype
      of those variables.
    . The default datatypes that Pseudo uses are:
      - number (which can contain integers or floats)
      - string
      - list
      - table
      - function
    . How you would store a variable named "x" into "all_variables" is like so:
      - interpret_state["all_variables"]["x"] = {"data_type": "number"}
    . Note that storing the value of the number is not mandatory because
      we let python do the evaluation and storage of the data to that
      variable name.
    . However, this doesn't mean that you can't store your own values into
      the variables. You can create your own values to store with your variables
      if you need them for other keywords that might use them.
      - For example: Say a keyword requires a variable that had a specific
        data called "password" and you have a keyword that creates a
        variable that contains a "password" data value, then you could do
        . all_variables = interpret_state[all_variables]
        . all_variables["some_key"] = {"data_type": "key", "password": "Pseudo"}
      - Note that the "data_type" value does not need to have the standard Pseudo
        datatype, it could be whatever you want it to be as long as it is
        compatible with your other keywords. It will not work if you decide to use
        this variable with Pseudo's keywords though so be mindful of that.
      - I mean, heck you can put whatever you want for that variable really. It's
        up to you to how you want to use it. For example:
        - interpret_state["all_variables"][some_var] = {"Some_datatype": "Don't Care"}
        - The above code is valid, just not compatible with Pseudo's keywords is all
      
  - "line_numb":
    . This holds the current line number of the Pseudo line. Although, it's actually
      the current line number - 1 since we are parsing each line in a list and lists
      are indexed at 0 while the line number for Pseudo is indexed at 1.
    . You can set the line number to any number you want and the parsing will jump
      to that line of Pseudo code. Think of this as a program counter. This number
      will automatically be incremented if you do not change it, if you do however
      the interpreter will start at that line when the current keyword is done. 
      Again, note that the line number in Pseudo is 1 more than line_numb.
    . For example, if you want to jump to line 20 in the Pseudo code, you can do this:
      - interpret_state[line_numb] = 19   # Pseudo line number - 1
      
  - "indent":
    . This holds the python indenation size, it is always 2. I recommend that you
      do not change its value as it is needed to successfully parse Pseudo's standard
      library keywords
      
  - "pseudo_indent":
    . This holds the indentation level of each Pseudo line (the number of spaces in front
      of the keyword). You'll need to combine this and the "indent" to make sure that
      the python code generated from your keyword parses successfully.
      
  - py_lines:
    . This holds a list of lines that will be printed directly to the output screen 
      of the GUI. You can append string that contain python code into here. There is no
      limit of how many lines you can append here. If your keyword requires 10 lines of
      python code to work, then you can append 10 lines of python to here. Just note that
      you will need to indent your lines so that python code can be executed successfully.
      This is why we have the "indent" and "pseudo_indent", the sum of the two is the
      actual indentation you will need to prepend your line first.
      
  - parse_success:
    . This holds the current evaluation state of the keyword being processed. For each
      keyword file you would need to return a True or False value. These values indicate
      whether a keyword has been successfully parsed. When returning either of those
      values, the interpreter will write them into interpret_state["parse_success"] and
      then it will check if the translation was completed. Inside your keyword file,
      it is RECOMMENDED that you do not modify this.
    
  - in_file_lines:
    . This holds a list of all of the lines of the Pseudo code. There's not much to say
      for this variable since we do not use it much in any of our basic keyword library.
      This is here for convience if you happen to need some line in the Pseudo code to
      work with the keyword being parsed.
      
  - keyword_dict:
    . This holds a dictionary that contains python modules for all keywords in the
      "interlib" folder. We use this for executing each keyword's handler() function.
      It is the reason why we can easily swap out keywords. You won't need to touch
      this variable at all unless you intend to run another keyword's handler()
      function. The only keyword in the basic library that utilizes this is the Import
      keyword, but it calls a utility function in utility.py that requires this variable.      
      
  - import_queue:
    . This contains a special list that holds all files that the main pseudo code wants to
      import. This is needed to check for circular imports and error out. Only the Import
      keyword utilizes this variable as of right now. I'm not sure when you will need to
      check for imports of other pseudo files, but if you do use this then modify at your
      own risk.
      
  - pseudo_filepath:
    . This contains a string that is the filepath directory of the main Pseudo code
      file that will be interpreted. This is also required because the Import keyword only
      has the ability to import files from the same directory as your main Pseudo code file.
      I would like to extend this functionality to import pseudo files from anywhere in
      the computer or even  import Pseudo code files within a given directory or filepath.
      Like the parse_success variable, it is RECOMMENDED that you do not touch this or else
      your imports will likely error out.

  - pseudo_file:
    . This contians a string of the actual Pseudo code file's name. This here is also used
      for the Import keyword to check a function is from this file or from the import file.
      Like pseudo_filepath, it is RECOMMENDED that you do not modify this.
      
  - plain_import_files:
    . This contains a list of filepaths to import to the translated Python code of the main
      Pseudo code. When we are executing the Python code that the main Pseudo code has 
      generated, the import keywords in the Python code will try to import those files. On
      an IDE this works fine, however when running this through a binary the file does not
      import for reasons that I can't explain thoroughly. Just note it is RECOMMENDED that
      you should not touch this at all.

  - is_debug_on:
    . This contains a boolean to indicate that "debug mode" is on/off when the GUI has toggled 
      it on/off. This is useful for developing your keywords locally on the GUI and not have
      to bother running the gui.py file through an IDE. You should use this in a try-except
      block in your keyword file so that raised exceptions specific to that keyword can be
      printed to the console. In order to print out raised exceptions, use the show_error()
      function that's in the utility.py file within your excpet block.
      
  

'''

'''
+-+-+-+- HELP MANUAL -+-+-+-+:
  . The help_manual variable is a long string that should contain your syntax and examples of
    how to use the keyword. You can take a look from the other keywords in the "interlib" folder
    to get an idea of what is to be expected. When saving this keyword file, it will be
    automatically updated to the Pseudo GUI's Help Document. If no help_manual is given, then
    the Help Document will display text stating that this keyword does not have a help manual.
    
  . Some rules to follow:
    - Use brackets [] when a word or phrase is optional
    - Use parentheses () when a word a phrase is mandatory
    - Use forward-slash / when multiple words or phrases can be selected, but only ONE can
      be selected
  
  . For example, check this sentence out:
    I (loved/[used to] love/will love) pie!
    Permutations of this sentence are:
      - I loved pie!
      - I used to love pie!
      - I love pie!
      - I will love pie!
  . Note that we are forced to chose only one of those phrases in the parentheses. Otherwise
    our sentence will not make any sense.
  . The bracket words [used to] are optional before the word "love" so if you were to omit
    the bracket words, it should have no affect in the structure of the sentence, but it
    will change the meaning of the sentence.
       
'''
help_manual = "  Syntax: \n" \
              "  Show [the] syntax of the keyword\n" \              
              "  \n" \
              "  Examples: \n" \
              "  \n"
              
'''
+-+-+-+- HANDLER -+-+-+-+:
  . The handler() function is required for any keyword file so that the interpreter can detect
    if this file's name is a valid keyword or not. What you do in here is up to you and how
    you want the python code to look like when your keyword statement is parsed successfully.
    Just remember that if you want to add python code to the python code file, append your
    python code statement to interpret_state["py_lines"]
'''
              
def handler(interpret_state):
  pass