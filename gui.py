import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from interpreter import interpret
import os
from datetime import datetime
from tkinter import filedialog as fd

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
      
      self.create_new()
      self.create_open()
      self.create_save()
      self.create_saveAs()
      self.create_settings()
      self.create_execute()

      self.filePointer = False
      self.filePointerName = ""
      self.settingsOpen = False

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
      self.save["command"] = lambda :self.save_file()
      self.save.pack(padx = 5, pady = 2, side = "left")

   def create_saveAs(self):
      self.saveAs = tk.Button(self.topframe) 
      self.saveAs["text"] = "Save As"
      self.saveAs["fg"] = "white"
      self.saveAs["bg"] = "#89CFF0"
      self.saveAs["activeforeground"] = "blue"
      self.saveAs["relief"] = "groove"
      self.saveAs["height"] = 1
      self.saveAs["width"] = 6
      self.saveAs["command"] = lambda :self.saveAs_file()
      self.saveAs.pack(padx = 5, pady = 2, side = "left")
    
   def create_open(self):
      self.open = tk.Button(self.topframe) 
      self.open["text"] = "Open"
      self.open["fg"] = "white"
      self.open["bg"] = "#89CFF0"
      self.open["activeforeground"] = "blue"
      self.open["relief"] = "groove"
      self.open["height"] = 1
      self.open["width"] = 4
      self.open["command"] = lambda :self.take_input_file()
      self.open.pack(padx = 5, pady = 2, side = "left")

   def create_new(self):
      self.new = tk.Button(self.topframe) 
      self.new["text"] = "New"
      self.new["fg"] = "white"
      self.new["bg"] = "#89CFF0"
      self.new["activeforeground"] = "blue"
      self.new["relief"] = "groove"
      self.new["height"] = 1
      self.new["width"] = 4
      self.new["command"] = lambda :self.new_file()
      self.new.pack(padx = 5, pady = 2, side = "left")

   def create_settings(self):
      self.settings = tk.Button(self.topframe) 
      self.settings["text"] = "Settings"
      self.settings["fg"] = "white"
      self.settings["bg"] = "#89CFF0"
      self.settings["activeforeground"] = "blue"
      self.settings["relief"] = "groove"
      self.settings["height"] = 1
      self.settings["width"] = 6
      self.settings["command"] = lambda :self.show_settings()
      self.settings.pack(padx = 5, pady = 2, side = "left")

   def show_settings(self):
      if not self.settingsOpen:
        self.settingsOpen = True
        tabWidth = 400
        tabHeight = 300

        parentStats = self.master.geometry().split('+')
        parentWidth = int(parentStats[0].split('x')[0])
        parentHeight = int(parentStats[0].split('x')[1])

        if root.state() == "zoomed":
          parentStats[1] = "0"
          parentStats[2] = "0"

        propperX = int(parentStats[1]) + int(parentWidth/2) - int(tabWidth/2);
        propperY = int(parentStats[2]) + int(parentHeight/2) - int(tabHeight/2);

        settingsTab = tk.Tk()
        settingsTab.geometry(str(tabWidth) + "x" + str(tabHeight)  + "+" + str(propperX) + "+" + str(propperY))
        settingsTab.title("Settings")
        settingsTab.wm_attributes("-topmost", 1)
        settingsTab.focus_force()

        def closeWindow():
          self.settingsOpen = False
          settingsTab.destroy()
        settingsTab.protocol("WM_DELETE_WINDOW", closeWindow)


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

   
   def take_input_file(self):
      file = fd.askopenfile(mode ='r', filetypes =[('Pseudo Files', '*.pseudo')])
      time = datetime.now()
      time = time.strftime('%H:%M %m/%d/%Y')

      if file is not None:
        content = file.read()
        self.input.delete('1.0', fd.END)
        self.input.insert(tk.INSERT, content)
        self.master.title("Pseudo " + file.name)
        self.filePointer = True
        self.filePointerName = file.name

        self.console.config(state = "normal")
        self.console.insert(tk.INSERT, "Opened " + os.path.basename(file.name) + " " + time + "\n")
        self.console.config(state = "disabled")
        file.close()

   #Saves file that is open
   #if no file is open then it will prompt for a save location and name for new file
   def save_file(self):
      file = None
      time = datetime.now()
      time = time.strftime('%H:%M %m/%d/%Y')

      if self.filePointer == True:
        file = open(self.filePointerName, "w")
        file.write(self.input.get("1.0","end-1c"))

      else:
        file = fd.asksaveasfile(filetypes = [('Pseudo Files', '*.pseudo')],
                                defaultextension = [('Pseudo Files', '*.pseudo')])
        if file is not None:
          file.write(self.input.get("1.0","end-1c"))
          self.master.title("Pseudo " + file.name)
          self.filePointer = True
          self.filePointerName = file.name

      if file is not None:
        self.console.config(state = "normal")
        self.console.insert(tk.INSERT, "Saved " + os.path.basename(file.name) + " " + time + "\n")
        self.console.config(state = "disabled")
        file.close()

   def saveAs_file(self):
    file = fd.asksaveasfile(filetypes = [('Pseudo Files', '*.pseudo')],
                            defaultextension = [('Pseudo Files', '*.pseudo')])
    time = datetime.now()
    time = time.strftime('%H:%M %m/%d/%Y')

    if file is not None:
      file.write(self.input.get("1.0","end-1c"))
      self.master.title("Pseudo " + file.name)
      self.filePointer = True
      self.filePointerName = file.name

      self.console.config(state = "normal")
      self.console.insert(tk.INSERT, "Saved " + os.path.basename(file.name) + "  " + time + "\n")
      self.console.config(state = "disabled")
      file.close()

   
   def new_file(self):
      self.master.title("Pseudo")
      self.filePointer = False
      self.filePointerName = ""
      self.input.delete('1.0', fd.END)
      self.output.delete('1.0', fd.END)

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
