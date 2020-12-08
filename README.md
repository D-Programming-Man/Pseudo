# Pseudo
An interpreter that translate English to python code. This project was inspired by a Minecraft Plugin called [Skript](https://github.com/SkriptLang/Skript) that allowed players to develop Minecraft Plugins without learning how to write Java code or managing a plugin project. It's intuitive syntax of writing down English phrases to usable code in the game is the same idea that Pseudo will have for users who will be writing down Pseudo code.

How Pseudo works in general is by writing down English words with some Python syntax to create Python code. How we achieve this is by the use of Keywords, words that start from the beginning of a line will indicate what code will be generated to a python file.

Psuedo really is a GUI/IDE in a sense and all documentation of Keywords is encapuslated into it.

Its most prominent feature is its ability to dynamically read Keyword files and intergrate it into the framework. This means that that if you want to add or expand more keywords, you are allowed to do so. Keyword are python files in the "interlib" folder used to translate lines of Pseudo code to Python code. The "interlib" folder is required to actually run the Pseudo program successfully and it needs to be in the same directory as the program. Download it to try out the basic Keywords we implmeneted to get the general idea of using Pseudo.

This project was made with the help of David Gmerek, Dvir Bar, Steven Resendiz, and Marlon Gergorio. Without them, I wouldn't have thought of implementing certain features for Pseudo.
