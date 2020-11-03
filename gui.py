import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from interpreter import interpret
import os
from datetime import datetime
from tkinter import filedialog as fd

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result       
class NumberedText(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

    def _on_change(self, event):
        self.linenumbers.redraw()

class Application(tk.Frame):
   def __init__(self, master=None):
      super().__init__(master)
      self.master = master
      master.title("Pseudo")
      master.geometry("720x480")
      self.pack()
      
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
      self.python_file_name = ""
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
      self.input = NumberedText(self.leftframe)
      self.input.pack(padx = 5, pady=2, fill = "both", expand = True)

   # Creates textbox for the python file
   def create_output_window(self):
      self.output = NumberedText(self.rightframe)
      self.output.text.config(state = "disabled")
      self.output.text.config(cursor = "arrow")
      self.output.pack(padx = 5, pady = 2, fill = "both", expand = True)

   # Create textbox for the console
   def create_console_window(self):
      self.console = tk.scrolledtext.ScrolledText(self.bottomframe, state = "disabled", cursor = "arrow", height = 6)
      self.console.pack(padx = 5, pady = 10, expand = True, fill = "x")

   # saves into pseudo file. Calls a print to console and python output
   def interpreter_func(self):
      self.save_file();
      interpret(self.filePointerName, self.python_file_name)
      self.print_to_output()
      self.read_to_console();

   # prints py file to right window
   def print_to_output(self):
      output = open(self.python_file_name, "r")
      self.output.text.config(state = "normal")
      self.output.text.delete("1.0", tk.END)
      self.output.text.insert(tk.INSERT, output.read())
      self.output.text.config(state = "disable")

   
   def take_input_file(self):
      file = fd.askopenfile(mode ='r', filetypes =[('Pseudo Files', '*.pseudo')])
      time = datetime.now()
      time = time.strftime('%H:%M %m/%d/%Y')

      if file is not None:
        content = file.read()
        self.input.text.delete('1.0', fd.END)
        self.input.text.insert(tk.INSERT, content)
        self.master.title("Pseudo " + file.name)
        self.filePointer = True
        self.filePointerName = file.name
        self.python_file_name = file.name[0:-6]+"py"

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
        file.write(self.input.text.get("1.0","end-1c"))

      else:
        file = fd.asksaveasfile(filetypes = [('Pseudo Files', '*.pseudo')],
                                defaultextension = [('Pseudo Files', '*.pseudo')])
        if file is not None:
          file.write(self.input.text.get("1.0","end-1c"))
          self.master.title("Pseudo " + file.name)
          self.filePointer = True
          self.filePointerName = file.name
          self.python_file_name = file.name[0:-6]+"py"

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
      file.write(self.input.text.get("1.0","end-1c"))
      self.master.title("Pseudo " + file.name)
      self.filePointer = True
      self.filePointerName = file.name
      self.python_file_name = file.name[0:-6]+"py"

      self.console.config(state = "normal")
      self.console.insert(tk.INSERT, "Saved " + os.path.basename(file.name) + "  " + time + "\n")
      self.console.config(state = "disabled")
      file.close()

   
   def new_file(self):
      self.master.title("Pseudo")
      self.filePointer = False
      self.filePointerName = ""
      self.python_file_name = ""
      self.input.text.delete('1.0', fd.END)
      self.output.text.delete('1.0', fd.END)

   
   # Reads the output.txt file and puts it into the console of the GUI
   def read_to_console(self):
      console_output = open( "output.txt" , "r")
      self.console.config(state = "normal")
      self.console.insert(tk.INSERT, console_output.read())
      self.console.config(state = "disable")


if __name__ == "__main__":
   root = tk.Tk()
   app = Application(master=root)
   app.mainloop()
