
# Pseudo 
###### *An interpreter that translates English to python code*
-----------------------

_*This project was made with the help of David Gmerek, Dvir Bar, Steven Resendiz, and Marlon Gergorio. Without them, I wouldn't have thought of implementing certain features for Pseudo.*_

-----------------

Pseudo is an interpreter language built on top of the Python language. It is presented as a GUI/IDE. Pseudo aims to teach you how to code like a programmer by writing down plain English. With Pseudo, learning how to code will be more simple than looking up tutorials of how to make your first "Hello World" program.

Pseudo works by writing down English words with some Python syntax to create Python code. How we achieve this is by the use of Keywords, words that start from the beginning of a line will indicate what code will be generated to a python file. All documentation of Keywords is encapuslated into it.

Its most prominent feature is its ability to dynamically read Keyword files and intergrate it into the framework. This means that if you want to add or expand more keywords, you are allowed to do so. Keywords are python files in the "interlib" folder used to translate lines of Pseudo code to Python code. The "interlib" folder is required to actually run the Pseudo program successfully and it needs to be in the same directory as the program. Download it to try out the basic Keywords we implmeneted to get the general idea of using Pseudo. 

For building the program yourself, it requires pyinstaller to build the binary in the console. The command to build it is:
`pyinstaller.exe --windowed --noconsole --onefile --name="Pseudo" gui.py`
- Just note that pyinstaller does not work with python 3.8 yet. Python 3.7.x and lower should be supported.

The Python language that we are using to build Pseudo is not that bad of a language for getting your feet wet in the world of programming. It's very easy to learn and the libraries are simple enough to get your head around. That's why we are using Python. Once you are comfortable with Pseudo, you can read the source code and familarize yourself with the features it implements.

 This project was inspired by a Minecraft Plugin called Skript that allowed players to develop Minecraft Plugins without learning how to write Java code or managing a plugin project. It's intuitive syntax of writing down English phrases to usable code in the game is the same idea that Pseudo will have for users who will be writing down Pseudo code.



## Let's explain how we write down Pseudo code.
---------------
Each beginning word is a 'Keyword'. Keywords are commands that you tell the Pseudo program to execute. The basic ones are `Create`, the aritmetic operators (`Add`, `Subtract`, `Multply`, and `Divide`), and `Display`.

Create: 
-------
The `Create` keyword will create a variable with the values you specify. How you would write it is like so:
>  `Create [a/an] <data type> named <variable name> with [a/an] (value/values) <value>`

Now this might seem confusing at first, so let us try to decode what all this means.
-  **Brackets** []: Brackets mean that the words inside of them are **OPTIONAL**. This means that they can be omitted from the phrase and still be sucessfully executed.

 - **Parentheses** (): Parentheses mean that the words inside of them are **MANDATORY**, but you can only chose **ONE** of them. If you omit them from the phrase, the Pseudo interpreter will complain.

- **Slash** /: What the slashes means is that you can choose any one of the options within [] or (), but you must ONLY chose one.

- **<data type>**: Is an internal mechanism that Pseudo does to keep track of data. For now, the only valid <data type>s are `variable`, `list`, and `table`. More <data type>s will be implemented later.
- **"variable"**: A "variable" can contain a number or a piece of text
 *(Technically, it can hold either an integer, float, or a string)*.
- **"list"**: A "list" is what you expect a list to be. A sequence of items in the order you put them in (More info on creating lists later).
- **"table"**: You can think of a "table" like an excel sheet. One entry of a table is used for one value (More info on creating tables later). 

>    Side note: "list" and "table" can contain other "list" and "table" values as well.

- **<variable name>**: This the name that will represent the data. This name is one word only, if you want to have two words for a variable name use underscores. 
  - E.g: `this variable` is not a valid name, but `this_variable` is.

 - **<value>**: If the <data type> is a "variable", then the only data you can store are numbers and text. If the <data type> is a list, then you can store list values. If the <data type> is a table, then table values are valid.
- **number**: This can be an integer or a rational number.
  - E.g: 1, 20, or 1.23212
- **text**: These values must be inbetween quotation marks (can be single or double quotation marks). 
   - E.g.: Both `'Text'` or `"Text"` will be valid values for a text.
 - **list**: A valid list value is surrounded by brackets [] with comma separeted values.
   - E.g: [1, 2, "Text"]

 >  Side note: The brackets for a list value are different from the brackets for the keywords. The brackets here are to differentiate from strings and tables so that they are directly parsed to python (When you translate your pseudo code, you'll see what we mean).

 - **table**: A valid table value is surrounded by braces {} with each entry separated by commas and a pair of values with colons inbetween. 
      - E.g: { "A": 1, "B": 2, "C": 3 }
 

## Let's try an example
---------------------
Say you want to create a variable named x with a value.
  We would type into the input window in the GUI like so:
 >   `Create a variable named x with a value 1`
 
 *Look at that!*
We just thought of what we wanted to do and then we just wrote it down in easy to understand english syntax.
It's just that easy. Let's do it agian with more examples:
>    `Create a variable named some_text with value "This is some text"`

>    `Create a variable named some_number with a value 10.2`

>  `Create a list named list_1 with values ["This", "is", "a", "list"]`

>    `Create a table named table_1 with a values {"Entry_1": 1, "Entry_2": 2}`

>    ` Create table named table_2 with value {"List": list_1, "Table:": table_1}`

      
*   This table will contain a list and a table inside of it



**Add and Multiply**:
This will allow you to add or multiply either numbers or variables that contain numbers together and store the result into a variable. 
Both of the keyword's syntax are:

> `(Add/Multiply) (<variable name>/<number>) and (<variable name>/<number>), store [it/the result] into <variable name>`

If you want to add two numbers, you can do it like so (given that you already created the variable to store it in.)
 > `Create a variable named x with a value 0
  Add 1 and 2, store the result into x`
  
This will mean that x will hold the value 3. You can also mix variables and numbers together like so:
>` Create a variable named x with a value 2
  Multiply x and 10, store it into x`
  
This will update x to be 20. The evaluation of the result will happen first, and then storing the result will happen after.



**Subtract**:
This syntax is very similar to the Add and Multiply syntax. Only one word is changed:
>`Subtract (<variable name>/<number>) from (<variable name>/<number>), store [it/the result] into <variable name>`

How the subtraction is handled is that the first (<variable name>/<number>) will be taken from the second (<variable name>/<number>). For example:
 >`Create a variable named x with a value 0
  Subtract 1 from 2, store it into x`

If we were to write this in an equation format, it would look like this: 2 - 1 = x



**Divide**:
This syntax is very similar to the Add and Multiply syntax. Only one word is changed:

>`Divide (<variable name>/<number>) by (<variable name>/<number>), store [it/the result] into <variable name>`

The divide statement is very similar to how fraction division looks like.
 >` Create a variable named x with a value 0
  Divide 20 by 10, store into x`

In an equation it'll look like this: 20 / 10 = x



**Display**:
This keyword will display things out to the output section of Pseudo (If running the interpreter through the console, then it would output things to the console. If you are using the GUI, then otuput to the GUI). Its syntax is:

>`Display (<variable name>/<text>)[, (<variable name>/<text>)][, (<variable name>/<text>)][...]`

What the syntax represents are comma separated values with a variable or text at each value. So let's say we want to display our result of the addition between two numbers. We would do it like so:
 >` Create a variable named result with value 0
  Add 1 and 2, store it into result
  Display result`
  
This will display 3 to the output section of the console/GUI. If you want to display multiple pieces of text to the output, then you would do it like so:
 >` Create a variable named world with a value "World"
  Display "Hello ", world, "!"`
  
Remember that any text value needs to have quotation marks surrounding the text you want to print out.
  
With this knowledge of how Pseudo works, you can now begin to code your frist "Hello World" program!



 ### HELLO WORLD
---------------
This is pretty easy. All Pseudo code needs to be written to the test.pseudo file (there are already some preloaded pseudo code in there for testing purposes, but feel free to look and delete everything if you want to). Knowing that you can display text to the console/GUI with the "Display" keyword you can do it like so:
>` Display "Hello World"`
  
Run the interpreter program and you should see your console/GUI output the text. The interpreter also writes the output to a file called output.txt 
Actually, the interpreter writes the output to the output.txt file first, then the interpreter reads the output.txt file and prints it to the console. And that's not all, all of your Pseudo code gets translated into Python code as well. You can view the equivalent code in a file called outfile.py. Just open it with a text editor (like notepad) and you can see what each line of code is equivalent to. Just ignore the `'if __name__  ==  "__main__": '` part since that is required by python to start the code.

