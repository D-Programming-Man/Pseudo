import sys
import os
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog as fd
from guilib.numberedtext import NumberedText
from interpreter import interpret
from datetime import datetime
from importlib import import_module


class Application(tk.Frame):
   def __init__(self, master=None):
      super().__init__(master)
      self.master = master
      master.title("Pseudo")
      #master.geometry("720x480")
      self.pack()
      
      # What this does is to dynamically import python files/modules from the "interlib" directory.
      # This means that we won't have to hardcode function names in the interpreter.py file,
      # adding more flexability to the interpreter
      base_lib = "interlib"
      keyword_py = [f for f in os.listdir(base_lib) if os.path.isfile(os.path.join(base_lib, f))]
  
      # Imports each keyword python file
      self.keyword_dict = {}
      for keyword_file in keyword_py:
         if keyword_file[-3:] != ".py":
            print(keyword_file + " is not a python file. Ignoring keyword.")
            continue
         keyword = keyword_file[0:-3]
         try:
            self.keyword_dict[keyword] = import_module(base_lib + "." + keyword, base_lib)
         except:
            print("Could not load the keyword file: " + keyword_file)
      
      # Create all aspects of the window
      self.create_frames()
      self.create_input_window()
      self.create_output_window()
      self.create_console_window()
      
      # Setting values needed for the menu
      self.show_python = tk.BooleanVar()
      self.show_python.set(True)
      self.gui_theme = tk.StringVar()
      self.gui_theme.set("normal")
      self.prev_theme = tk.StringVar()
      self.prev_theme.set("")
      self.normal_theme = tk.BooleanVar()
      self.dark_theme = tk.BooleanVar()
      self.normal_theme.set(True)
      self.dark_theme.set(False)
      
      self.is_live_interpreting = tk.BooleanVar()
      self.is_live_interpreting.set(False)
      
      # Menu that contains all of the functions of the buttons and more
      self.create_menu()
      

      self.filePointer = False
      self.filePointerName = ""
      self.python_file_name = ""
      self.settingsOpen = False
      self.fontList = ("Courier", "Times", "Helvetica", "Comic Sans MS")
      self.font = "Helvetica"
      self.fontValue = 0
      self.fontSize = 10
      
      self.rgb_value = [0,0,0]

      self.is_save_load_prompt = False

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

   def close_settings(self):
    self.settingsOpen = False
    self.settingsTab.destroy()

   def update_settings(self):
    if self.settingsTab.fontValue != None:
      self.font = self.fontList[self.settingsTab.fontValue]
      self.fontValue = self.settingsTab.fontValue

    if self.settingsTab.fontSize != None:
      self.fontSize = self.settingsTab.fontSize

    #Updating fonts
    self.input.text.config(font = (self.font, self.fontSize))
    self.output.text.config(font = (self.font, self.fontSize))
    self.console.config(font = (self.font, self.fontSize))
    self.input.linenumbers.setFont(self.font, self.fontSize)
    self.output.linenumbers.setFont(self.font, self.fontSize)
    self.output.linenumbers.redraw()
    self.input.linenumbers.redraw()
    
    self.close_settings()

   def show_settings(self):
      if not self.settingsOpen:
        self.settingsOpen = True
        tabWidth = 400
        tabHeight = 300
        parentStats = self.master.geometry().split('+')
        parentWidth = int(parentStats[0].split('x')[0])
        parentHeight = int(parentStats[0].split('x')[1])

        #If maximized window, will assume parent is at x = 0, y = 0
        if self.master.state() == "zoomed":
          parentStats[1] = "0"
          parentStats[2] = "0"

        #Calculates x and y values for settings window to be centered
        propperX = int(parentStats[1]) + int(parentWidth/2) - int(tabWidth/2);
        propperY = int(parentStats[2]) + int(parentHeight/2) - int(tabHeight/2);

        #Basic setttings window structure
        self.settingsTab = tk.Tk()
        self.settingsTab.geometry(str(tabWidth) + "x" + str(tabHeight)  + "+" + str(propperX) + "+" + str(propperY))
        self.settingsTab.title("Settings")
        self.settingsTab.wm_attributes("-topmost", 1)
        self.settingsTab.focus_force()
        self.settingsTab.protocol("WM_DELETE_WINDOW", self.close_settings)
        self.settingsTab["bg"] = "#FEF9DA"
        self.settingsTab.fontValue = None
        self.settingsTab.fontSize = None

        #Event handler for the font dropdown
        def onFontSelect(event):
          self.settingsTab.fontValue = fontDropdown.current()
          self.settingsTab.focus()

        #Event handler for the font size slider
        def onFontSize(event):
          self.settingsTab.fontSize = fontSlider.get()
        
        #Options to adjust settings in top frame
        topFrame = tk.Frame(self.settingsTab)
        topFrame.pack(pady = 20)
        
        fontLabel = tk.Label(topFrame, text = "Font")
        fontDropdown = ttk.Combobox(topFrame, values = self.fontList, state = "readonly")
        fontDropdown.current(self.fontValue)
        fontDropdown.bind("<<ComboboxSelected>>", onFontSelect)
        
        fontSizeLabel = tk.Label(topFrame, text = "Font Size")
        fontSlider = tk.Scale(topFrame, from_= 6, to = 30, orient = tk.HORIZONTAL)
        fontSlider.set(self.fontSize)
        fontSlider.bind("<ButtonRelease-1>", onFontSize)

        #Backround colors of settings options
        fontSlider.config(bg = "#FEF9DA")
        fontSizeLabel.config(bg="#FEF9DA")
        fontLabel.config(bg = "#FEF9DA")
        topFrame.config(bg = "#FEF9DA")

        #Locations where the settings objects are
        fontLabel.grid(column = 0, row = 0, padx = 25, sticky = tk.W)
        fontDropdown.grid(column = 2, row = 0, padx = 25)
        fontSizeLabel.grid(column = 0, row = 1, padx = 25, sticky = tk.W)
        fontSlider.grid(column = 2, row = 1, padx = 25, ipadx = 20)

        #Save and cancel button in bottom frame
        bottomFrame = tk.Frame(self.settingsTab)
        bottomFrame.pack(side = tk.BOTTOM, pady = 20)
        bottomFrame.config(bg = "#FEF9DA")
        
        savebutton = tk.Button(bottomFrame, text = "Save", fg = "black", command = self.update_settings)
        savebutton.pack(side = tk.LEFT, padx = 10)
        cancelbutton = tk.Button(bottomFrame, text = "Cancel", fg = "black", command = self.close_settings)
        cancelbutton.pack(side = tk.LEFT, padx = 10)

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
      
   # Functions that clear text
   def clear_input_window(self):
      self.input.text.delete('1.0', tk.END)

   def clear_output_window(self):
      self.output.text.config(state="normal")
      self.output.text.delete('1.0', tk.END)
      self.output.text.config(state="disable")

   def clear_console_window(self):
      self.console.config(state="normal")
      self.console.delete('1.0', tk.END)
      self.console.config(state="disabled")

   # saves into pseudo file. Calls a print to console and python output
   def interpreter_func(self):
      # Maybe have a toggle to enable library updates in here so that when
      # a user wants to develop their own keyword, then they can live test it
      # and not have to exit out of the application to load it in.
      base_lib = "interlib"
      keyword_py = [f for f in os.listdir(base_lib) if os.path.isfile(os.path.join(base_lib, f))]
  
      # Imports each keyword python file
      self.keyword_dict = {}
      for keyword_file in keyword_py:
         if keyword_file[-3:] != ".py":
            print(keyword_file + " is not a python file. Ignoring keyword.")
            continue
         keyword = keyword_file[0:-3]
         try:
            self.keyword_dict[keyword] = import_module(base_lib + "." + keyword, base_lib)
         except:
            print("Could not load the keyword file: " + keyword_file)
       
      self.save_file()
      interpret(self.filePointerName, self.python_file_name, self.keyword_dict)
      self.input.text.highlighter()
      self.clear_console_window()
      self.print_to_output()
      self.read_to_console()

   # prints py file to right window
   def print_to_output(self):
      
      output = open(self.python_file_name, "r")
      self.output.text.config(state="normal")
      self.output.text.delete("1.0", tk.END)
      self.output.text.insert(tk.INSERT, output.read())
      self.output.text.highlighter()
      self.output.text.config(state="disable")

   
   def take_input_file(self):
      self.is_save_load_prompt = True
      file = fd.askopenfile(mode ='r', filetypes =[('Pseudo Files', '*.pseudo')])
      time = datetime.now()
      time = time.strftime('%H:%M %m/%d/%Y')

      if file is not None:
        content = file.read()
        self.input.text.delete('1.0', fd.END)
        self.input.text.insert(tk.INSERT, content)

        self.input.text.highlighter()

        self.master.title("Pseudo " + file.name)
        self.filePointer = True
        self.filePointerName = file.name
        self.python_file_name = file.name[0:-6]+"py"

        self.console.config(state = "normal")
        self.console.insert(tk.INSERT, "Opened " + os.path.basename(file.name) + " " + time + "\n")
        self.console.config(state = "disabled")
        file.close()
      self.is_save_load_prompt = False
      if self.is_live_interpreting.get():
        self.live_interpret()

   #Saves file that is open
   #if no file is open then it will prompt for a save location and name for new file
   def save_file(self):
      file = None
      time = datetime.now()
      time = time.strftime('%H:%M %m/%d/%Y')
      self.is_save_load_prompt = True

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
      self.is_save_load_prompt = False

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
    self.is_save_load_prompt = False
   
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

   # Runs the interpret_func() every 1 second
   # Is toggled by the "Live Update" menu option under Run
   def live_interpret(self):
      # Set of conditions when we should update
      if self.is_save_load_prompt or not self.filePointer or not self.is_live_interpreting.get():
          return
      threading.Timer(1, self.live_interpret).start()
      
      # Only run the interpret function when the input text changes
      if not self.input.has_changed:
          return
      self.console.config(state = "normal")
      self.console.delete("1.0", tk.END)
      self.console.config(state = "disable")
      self.interpreter_func()
      self.input.has_changed = False

   def create_menu(self):
      menubar = tk.Menu(self.master)
      self.rightClick = tk.Menu(self.master, tearoff=0)

      # File menu
      filemenu = tk.Menu(menubar, tearoff=0)
      filemenu.add_command(label="New", command=lambda :self.new_file())
      filemenu.add_command(label="Open...", command=lambda :self.take_input_file(), accelerator="Ctrl+O")
      filemenu.add_command(label="Save", command=lambda :self.save_file(), accelerator="Ctrl+S")
      filemenu.add_command(label="Save As...", command=lambda :self.saveAs_file())
      filemenu.add_separator()
      filemenu.add_command(label="Exit", command=lambda :self.exit_pseudo(), accelerator="Esc")
      menubar.add_cascade(label="File", menu=filemenu)
      
      # Edit menu
      editmenu = tk.Menu(menubar, tearoff=0)
      editmenu.add_command(label="Settings", command=lambda :self.show_settings())
      filemenu.add_separator()
      menubar.add_cascade(label="Edit", menu=editmenu)

      # Run menu
      runmenu = tk.Menu(menubar, tearoff=0)
      runmenu.add_command(label="Execute", command=lambda :self.interpreter_func(), accelerator="F5")
      runmenu.add_checkbutton(label="Live Update", onvalue=1, offvalue=0, variable=self.is_live_interpreting, command=self.live_interpret)
      menubar.add_cascade(label="Run", menu=runmenu)
      
      # window menu
      windowmenu = tk.Menu(menubar, tearoff=0)
      windowmenu.add_checkbutton(label="Python Window", onvalue=1, offvalue=0, variable=self.show_python, command=self.toggle_python_window)
      menubar.add_cascade(label="Window", menu=windowmenu)
      
      # theme menu
      thememenu = tk.Menu(menubar, tearoff=0)
      thememenu.add_checkbutton(label="Normal", onvalue=1, offvalue=0, variable=self.normal_theme, command=lambda: self.set_theme("normal"))
      thememenu.add_checkbutton(label="Dark", onvalue=1, offvalue=0, variable=self.dark_theme, command=lambda: self.set_theme("dark"))
      menubar.add_cascade(label="Theme", menu=thememenu)
      
      # clear menu
     
      clearmenu = tk.Menu(menubar, tearoff=0)
      clearmenu.add_command(label="Console", command=lambda: self.clear_console_window(), accelerator="F8")
      clearmenu.add_command(label="Input", command=lambda: self.clear_input_window(), accelerator="F9")
      clearmenu.add_command(
          label="Output", command=lambda: self.clear_output_window(), accelerator="F10")

      menubar.add_cascade(label="Clear", menu=clearmenu)
      self.rightClick.add_cascade(label="Clear", menu=clearmenu)
        
      # Specific style configurations, currently a child of the theme menu.
      configMenu = tk.Menu(thememenu, tearoff=0)
      thememenu.add_cascade(label="Config", menu=configMenu)
      rgbMenu = tk.Menu(configMenu, tearoff=0)
      configMenu.add_cascade(label="RGB menu", menu=rgbMenu)
      rgbMenu.add_command(
          label="RGB Scale", command=lambda: self.show_scale_window())

      backgroundOption = tk.Menu(configMenu, tearoff=0)
      configMenu.add_cascade(label="Background", menu=backgroundOption)
      backgroundOption.add_command(label="Red", command=lambda: self.set_background_color("red"))
      backgroundOption.add_command(label="Blue", command=lambda: self.set_background_color("blue"))
      backgroundOption.add_command(label="Green", command=lambda: self.set_background_color("green"))
      backgroundOption.add_command(
          label="Yellow", command=lambda: self.set_background_color("yellow"))

      inputOption = tk.Menu(configMenu, tearoff=0)
      configMenu.add_cascade(label="Input", menu=inputOption)
      inputOption.add_command(
          label="Background")
      inputOption.add_command(
          label="White", command=lambda: self.set_input_bg("white"))
      inputOption.add_command(
          label="Red", command=lambda: self.set_input_bg("red"))
      inputOption.add_command(
          label="Blue", command=lambda: self.set_input_bg("blue"))
      inputOption.add_command(
          label="Green", command=lambda: self.set_input_bg("green"))
      inputOption.add_command(
          label="Yellow", command=lambda: self.set_input_bg("yellow"))
      inputOption.add_separator()
      inputOption.add_command(label="Text")
      inputOption.add_command(
          label="White", command=lambda: self.set_input_fg("white"))
      inputOption.add_command(
          label="Red", command=lambda: self.set_input_fg("red"))
      inputOption.add_command(
          label="Blue", command=lambda: self.set_input_fg("blue"))
      inputOption.add_command(
          label="Green", command=lambda: self.set_input_fg("green"))
      inputOption.add_command(
          label="Yellow", command=lambda: self.set_input_fg("yellow"))

      consoleOption = tk.Menu(configMenu, tearoff=0)
      configMenu.add_cascade(label="Console", menu=consoleOption)
      consoleOption.add_command(
          label="Background")
      consoleOption.add_command(
          label="White", command=lambda: self.set_console_bg("white"))
      consoleOption.add_command(
          label="Red", command=lambda: self.set_console_bg("red"))
      consoleOption.add_command(
          label="Blue", command=lambda: self.set_console_bg("blue"))
      consoleOption.add_command(
          label="Green", command=lambda: self.set_console_bg("green"))
      consoleOption.add_command(
          label="Yellow", command=lambda: self.set_console_bg("yellow"))
      consoleOption.add_separator()
      consoleOption.add_command(label="Text")
      consoleOption.add_command(
          label="White", command=lambda: self.set_console_fg("white"))
      consoleOption.add_command(
          label="Red", command=lambda: self.set_console_fg("red"))
      consoleOption.add_command(
          label="Blue", command=lambda: self.set_console_fg("blue"))
      consoleOption.add_command(
          label="Green", command=lambda: self.set_console_fg("green"))
      consoleOption.add_command(
          label="Yellow", command=lambda: self.set_console_fg("yellow"))

      outputOption = tk.Menu(configMenu, tearoff=0)
      configMenu.add_cascade(label="Output", menu=outputOption)
      outputOption.add_command(
          label="Background")
      outputOption.add_command(
          label="White", command=lambda: self.set_output_bg("white"))
      outputOption.add_command(
          label="Red", command=lambda: self.set_output_bg("red"))
      outputOption.add_command(
          label="Blue", command=lambda: self.set_output_bg("blue"))
      outputOption.add_command(
          label="Green", command=lambda: self.set_output_bg("green"))
      outputOption.add_command(
          label="Yellow", command=lambda: self.set_output_bg("yellow"))
      outputOption.add_separator()
      outputOption.add_command(label="Text")
      outputOption.add_command(
          label="White", command=lambda: self.set_output_fg("white"))
      outputOption.add_command(
          label="Red", command=lambda: self.set_output_fg("red"))
      outputOption.add_command(
          label="Blue", command=lambda: self.set_output_fg("blue"))
      outputOption.add_command(
          label="Green", command=lambda: self.set_output_fg("green"))
      outputOption.add_command(
          label="Yellow", command=lambda: self.set_output_fg("yellow"))

      # Create sortcuts for some options
      self.bind_all("<F5>", self.run_key)
      self.bind_all("<Control-o>", self.open_key)
      self.bind_all("<Control-s>", self.save_key)
      self.bind_all("<Escape>", self.exit_key)
      self.bind_all("<F8>", self.clear_console_key)
      self.bind_all("<F9>", self.clear_input_key)
      self.bind_all("<F10>", self.clear_output_key)
      self.bind_all("<Button-3>", self.pop_up_menu)

      # Pack all menu options and display it
      self.master.config(menu=menubar)

   def pop_up_menu(self, event):
    try:
        self.rightClick.tk_popup(event.x_root, event.y_root)
    finally:
        self.rightClick.grab_release()
   # New small functions for the menu options
   def newfile_key(self, event):
       self.new_file()
      
   def run_key(self, event):
      self.interpreter_func()

   def open_key(self, event):
      self.take_input_file()
      
   def save_key(self, event):
      self.save_file()
      
   def clear_console_key(self, event):
      self.clear_console_window()
   def clear_input_key(self, event):
      self.clear_input_window()
   def clear_output_key(self, event):
      self.clear_output_window()
      
   def exit_pseudo(self):
       self.exit_key("Escape")
      
   def exit_key(self, event):
       sys.exit(0)
# Window for RGB scales to choose color scheme
# Radiobuttons allow users to select what they want to change, currently options are{Background,Input,Output,Console,Text}
   def show_scale_window(self):
    self.scaleWindow = tk.Tk()
    self.scaleWindow.title('My Window')
    self.scaleWindow.geometry('500x300')

    self.selection = tk.IntVar(self.scaleWindow, value = 6, name = "optionVar")
    self.selection.set(0)
    self.l = tk.Label(self.scaleWindow, bg='white',
                      fg='black', width=20, text=self.selection.get())
    self.l.pack(anchor=tk.N)
    r1 = tk.Radiobutton(self.scaleWindow, text="Background",
                        variable=self.selection, value=1)
    r1.pack(anchor = tk.W)
    print(self.selection.get())

    r2 = tk.Radiobutton(self.scaleWindow, text="Input",
                        variable=self.selection, value=2)

    r2.pack(anchor = tk.W)
    print(self.selection.get())

    r3 = tk.Radiobutton(self.scaleWindow, text="Output",
                        variable=self.selection, value=3)
    r3.pack(anchor = tk.W)
    print(self.selection.get())

    r4 = tk.Radiobutton(
        self.scaleWindow, text="Console", variable=self.selection, value=4)
    r4.pack(anchor=tk.W)

    r5 = tk.Radiobutton(
        self.scaleWindow, text="Text", variable=self.selection, value=5)
    r5.pack(anchor=tk.W)

    r6 = tk.Radiobutton(
        self.scaleWindow, text="Keywords", variable=self.selection, value=6)
    r6.pack(anchor=tk.W)

    r7 = tk.Radiobutton(
        self.scaleWindow, text="Data types", variable=self.selection, value=7)
    r7.pack(anchor=tk.W)

    r8 = tk.Radiobutton(
        self.scaleWindow, text="Strings", variable=self.selection, value=8)
    r8.pack(anchor=tk.W)
    print(self.selection.get())

    self.r_var = tk.IntVar()
    self.b_var = tk.IntVar()
    self.g_var = tk.IntVar()
    self.Rscale = tk.Scale(self.scaleWindow, label='R', from_=0, to=255, orient=tk.HORIZONTAL, length=255,
                           showvalue=0, tickinterval=1, resolution=1, variable=self.r_var, command=self.red_color_scale)
    self.Rscale.place(x=100, y=25)
    self.Bscale = tk.Scale(self.scaleWindow, label='B', from_=0, to=255, orient=tk.HORIZONTAL, length=255,
                           showvalue=0, tickinterval=1, resolution=1, variable=self.b_var, command=self.blue_color_scale)
    self.Bscale.place(x=100, y=65)
    self.Gscale = tk.Scale(self.scaleWindow, label='G', from_=0, to=255, orient=tk.HORIZONTAL, length=255,
                           showvalue=0, tickinterval=1, resolution=1, variable=self.g_var, command=self.green_color_scale)
    self.Gscale.place(x=100, y=105)
    self.pack()
    
# depending on what which radiobutton selected the color for it will be changed
# this function takes in a hex color number passed from the scale functions
   def selected_option(self, mycolor):
    if self.selection.get() == 1:
        self.topframe.configure(background=mycolor)
        self.bottomframe.configure(background=mycolor)
        self.leftframe.configure(background=mycolor)
        self.rightframe.configure(background=mycolor)
    elif self.selection.get() == 2:
        self.input.text.configure(background=mycolor)
    elif self.selection.get() == 3:
        self.output.text.configure(background=mycolor)
    elif self.selection.get() == 4:
        self.console.configure(background=mycolor)
    elif self.selection.get() == 5:
        self.output.text.configure(foreground=mycolor)
        self.input.text.configure(foreground=mycolor)
        self.console.configure(foreground=mycolor)
    elif self.selection.get() == 6:
        self.input.text.tag_configure("keyword", foreground=mycolor)
        self.output.text.tag_configure("keyword", foreground=mycolor)
        self.input.text.highlighter()
        self.output.text.highlighter()
    elif self.selection.get() == 7:
        self.input.text.tag_configure("datatype", foreground=mycolor)
        self.output.text.tag_configure("datatype", foreground=mycolor)
        self.input.text.highlighter()
        self.output.text.highlighter()
    elif self.selection.get() == 8:
        self.input.text.tag_configure("string", foreground=mycolor)
        self.output.text.tag_configure("string", foreground=mycolor)
        self.input.text.highlighter()
        self.output.text.highlighter()

# functions for each scale r b g
   def red_color_scale(self, event):
        scalevalue = int(event)
        self.rgb_value[0] = scalevalue
        mycolor = '#%02x%02x%02x' % (
            self.rgb_value[0], self.rgb_value[1], self.rgb_value[2])
        self.selected_option(mycolor)

   def blue_color_scale(self, event):
        scalevalue = int(event)
        self.rgb_value[2] = scalevalue
        mycolor = '#%02x%02x%02x' % (
            self.rgb_value[0], self.rgb_value[1], self.rgb_value[2])
        self.selected_option(mycolor)

   def green_color_scale(self, event):
        scalevalue = int(event)
        self.rgb_value[1] = scalevalue
        mycolor = '#%02x%02x%02x' % (
            self.rgb_value[0], self.rgb_value[1], self.rgb_value[2])
        self.selected_option(mycolor)

   def toggle_python_window(self):
       if (self.show_python.get() == False):
           self.output.pack_forget()
       else:
           self.output.pack(padx = 5, pady = 2, fill = "both", expand = True)

   def set_input_bg(self, bgColor):
      self.input.text.configure(background=bgColor)
   def set_input_fg(self, fgColor):
      self.input.text.configure(foreground=fgColor)

   def set_output_bg(self, bgColor):
      self.output.text.configure(background=bgColor)
   def set_output_fg(self, fgColor):
      self.output.text.configure(foreground=fgColor)

   def set_console_bg(self, bgColor):
      self.console.configure(background=bgColor)
   def set_console_fg(self, fgColor):
      self.console.configure(foreground = fgColor)

   def set_background_color(self, color):
      self.topframe["bg"] = color
      self.bottomframe["bg"] = color
      self.leftframe["bg"] = color
      self.rightframe["bg"] = color
    
   def set_theme(self, theme):
      # 6E7074 = Dark Background
      # 45474B = Dark Text Background
      # NOTE: insertbackground is the text cursor color, NOT mouse cursor color
      #       background is the background color for the text wigit
      #       foreground is the text's color of that wigit
      if self.normal_theme.get() == False and self.dark_theme.get() == False:

         self.normal_theme.set(True)
         self.dark_theme.set(False)
         self.gui_theme.set("normal")
         self.topframe["bg"] = "#FEF9DA"
         self.bottomframe["bg"] = "#FEF9DA"
         self.leftframe["bg"] = "#FEF9DA"
         self.rightframe["bg"] = "#FEF9DA"
         self.input.text.configure(background="white", foreground="black", insertbackground="black")
         self.input.text.tag_configure("keyword", foreground="red")
         self.input.text.tag_configure("datatype", foreground="blue")
         self.input.text.tag_configure("string", foreground="green")

         self.output.text.configure(background="white", foreground="black", insertbackground="black")
         self.output.text.tag_configure("keyword", foreground="red")
         self.output.text.tag_configure("datatype", foreground="blue")
         self.output.text.tag_configure("string", foreground="green")

         self.console.configure(background="white", foreground="black")
         return
      
      if (theme == "normal"):
         self.gui_theme.set("normal")
         self.normal_theme.set(True)
         self.dark_theme.set(False)
         self.topframe["bg"] = "#FEF9DA"
         self.bottomframe["bg"] = "#FEF9DA"
         self.leftframe["bg"] = "#FEF9DA"
         self.rightframe["bg"] = "#FEF9DA"
         self.input.linenumbers.configure(background = "#E4E4E4", highlightbackground = "#E4E4E4")
         self.input.linenumbers.fill = "black"
         self.input.linenumbers.redraw()
         self.input.text.configure(background="white", foreground="black", insertbackground="black")
         self.input.text.tag_configure("keyword", foreground="red")
         self.input.text.tag_configure("datatype", foreground="blue")
         self.input.text.tag_configure("string", foreground="green")
         self.input.text.highlighter()

         self.output.linenumbers.configure(background = "#E4E4E4", highlightbackground = "#E4E4E4")
         self.output.linenumbers.fill = "black"
         self.output.linenumbers.redraw()
         self.output.text.configure(background="white", foreground="black", insertbackground="black")
         self.output.text.tag_configure("keyword", foreground="red")
         self.output.text.tag_configure("datatype", foreground="blue")
         self.output.text.tag_configure("string", foreground="green")
         self.output.text.highlighter()

         self.console.configure(background="white", foreground="black")
      
      if (theme == "dark"):
         self.gui_theme.set("dark")
         self.normal_theme.set(False)
         self.dark_theme.set(True)
         self.topframe["bg"] = "#6E7074"
         self.bottomframe["bg"] = "#6E7074"
         self.leftframe["bg"] = "#6E7074"
         self.rightframe["bg"] = "#6E7074"
         self.input.linenumbers.configure(background = "#616161", highlightbackground = "#616161")
         self.input.linenumbers.fill = "white"
         self.input.linenumbers.redraw()
         self.input.text.configure(background="#45474B", foreground="white", insertbackground="white")
         self.input.text.tag_configure("keyword", foreground="orange")
         self.input.text.tag_configure("datatype", foreground="lightblue")
         self.input.text.tag_configure("string", foreground="lightgreen")
         self.input.text.highlighter()

         self.output.linenumbers.configure(background = "#616161", highlightbackground = "#616161")
         self.output.linenumbers.fill = "white"
         self.output.linenumbers.redraw()
         self.output.text.configure(background="#45474B", foreground="white", insertbackground="white")
         self.output.text.tag_configure("keyword", foreground="orange")
         self.output.text.tag_configure("datatype", foreground="lightblue")
         self.output.text.tag_configure("string", foreground="lightgreen")
         self.output.text.highlighter()

         self.console.configure(background="#45474B", foreground="white")
