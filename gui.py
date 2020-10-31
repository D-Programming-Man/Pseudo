import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from interpreter import interpret

#hardcode file_names
INPUT = "test.pseudo"
PY_FILE = "outfile.py"
OUTPUT = "output.txt"

class Application(tk.Frame):
   def __init__(self, master=None):
      super().__init__(master)
      self.master = master
      master.title("Pseudo")
      master.geometry("720x480")
      self.pack()
      
      # Save file names into object 
      self.input_file = INPUT
      self.py_file = PY_FILE
      self.output_file = OUTPUT

      # Create all aspects of the window
      self.create_frames()
      self.create_input_window()
      self.create_output_window()
      self.create_console_window()
      self.create_execute()
      self.create_save()

   # Creates frames: top, left, right, bottom. Each holds widgets
   def create_frames(self):
      self.topframe = tk.Frame(self.master, bg = "#FEF9DA")
      self.topframe.pack(side = "top", fill = "both")
      self.bottomframe = tk.Frame(self.master, bg = "#FEF9DA")
      self.bottomframe.pack(side = "bottom", fill = "both")
      self.leftframe = tk.Frame(self.master, bg = "#FEF9DA")
      self.leftframe.pack(side = "left", fill = "both", expand = True)
      self.rightframe = tk.Frame(self.master, bg = "#FEF9DA")
      self.rightframe.pack(side = "right", fill = "both", expand = True)

   # Creates button widget which runs the interpreter
   def create_execute(self):
      self.execute = tk.Button(self.topframe, command = lambda:self.unit_test_print()) 
      self.execute["text"] = "Run"
      self.execute["fg"] = "white"
      self.execute["bg"] = "#89CFF0"
      self.execute["activeforeground"] = "blue"
      self.execute["relief"] = "groove"
      self.execute["height"] = 1
      self.execute["width"] = 4
      self.execute["command"] = lambda :self.interpreter_func()
      self.execute.pack(padx = 5, pady = 2, side = "left")

   # Creates button widget which runs save_func
   def create_save(self):
      self.save = tk.Button(self.topframe) 
      self.save["text"] = "Save"
      self.save["fg"] = "white"
      self.save["bg"] = "#89CFF0"
      self.save["activeforeground"] = "blue"
      self.save["relief"] = "groove"
      self.save["height"] = 1
      self.save["width"] = 4
      self.save["command"] = lambda :self.test_print()
      self.save.pack(pady = 2, side = "left")

   # Creates textbox to receive user input
   def create_input_window(self):
      self.input = tk.scrolledtext.ScrolledText(self.leftframe)
      self.input.pack(padx = 5, pady=2, fill = "both", expand = True)

   # Creates textbox for the python file
   def create_output_window(self):
      self.output = tk.scrolledtext.ScrolledText(self.rightframe, state = "disabled", cursor = "arrow")
      self.output.pack(padx = 5, pady = 2, fill = "both", expand = True)

   # Create textbox for the console
   def create_console_window(self):
      self.console = tk.scrolledtext.ScrolledText(self.bottomframe, state = "disabled", cursor = "arrow", height = 6)
      self.console.pack(padx = 5, pady = 10, expand = True, fill = "x")

   #test to demonstrate how to print(can be deleted)
   def test_print(self):
      if(self.input.get("1.0","end-1c" ) == "hi"):
         self.output.config(state = "normal")
         self.output.insert(tk.INSERT, "hello ")
         self.output.config(state = "disabled")

   # saves into pseudo file. Calls a print to console and python output
   def interpreter_func(self):
      self.save_load_func();
      interpret(self.input_file, self.py_file)
      self.print_to_output()
      self.read_to_console();

   # prints py file to right window
   def print_to_output(self):
      output = open(self.py_file, "r")
      self.output.config(state = "normal")
      self.output.delete("1.0", tk.END)
      self.output.insert(tk.INSERT, output.read())
      self.output.config(state = "disable")

   #
   def save_load_func(self):
      pass
   
   # Reads the output.txt file and puts it into the console of the GUI
   def read_to_console(self):
      console_output = open( self.output_file , "r")
      self.console.config(state = "normal")
      self.console.delete("1.0", tk.END)
      self.console.insert(tk.INSERT, console_output.read())
      self.console.config(state = "disable")


if __name__ == "__main__":
   root = tk.Tk()
   app = Application(master=root)
   app.mainloop()
