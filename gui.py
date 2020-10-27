import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk

#hardcode file_names
input_file = ""
output_file = ""

class Application(tk.Frame):
   def __init__(self, master=None):
      super().__init__(master)
      self.master = master
      master.title("Pseudo")
      master.geometry("720x480")
      self.pack()

      self.create_frames()
      self.create_input_window()
      self.create_output_window()
      self.create_console_window()
      self.create_execute()
      self.create_save()

   def create_frames(self):
      self.topframe = tk.Frame(self.master, bg = "#FEF9DA")
      self.topframe.pack(side = "top", fill = "both")
      self.bottomframe = tk.Frame(self.master, bg = "#FEF9DA")
      self.bottomframe.pack(side = "bottom", fill = "both")
      self.leftframe = tk.Frame(self.master, bg = "#FEF9DA")
      self.leftframe.pack(side = "left", fill = "both", expand = True)
      self.rightframe = tk.Frame(self.master, bg = "#FEF9DA")
      self.rightframe.pack(side = "right", fill = "both", expand = True)

   def create_execute(self):
      self.execute = tk.Button(self.topframe, command = lambda:self.unit_test_print()) 
      self.execute["text"] = "Execute"
      self.execute["fg"] = "white"
      self.execute["bg"] = "#89CFF0"
      self.execute["activeforeground"] = "blue"
      self.execute["relief"] = "groove"
      self.execute["height"] = 2
      self.execute["width"] = 5
      self.execute["command"] = lambda :self.test_print()
      self.execute.pack(padx = 5, pady = 2, side = "left")
 
   def create_save(self):
      self.save = tk.Button(self.topframe, command = lambda:self.test_print()) 
      self.save["text"] = "Save"
      self.save["fg"] = "white"
      self.save["bg"] = "#89CFF0"
      self.save["activeforeground"] = "blue"
      self.save["relief"] = "groove"
      self.save["height"] = 2
      self.save["width"] = 5
      self.save["command"] = lambda :self.test_print()
      self.save.pack(pady = 2, side = "left")

   def create_input_window(self):
      self.input = tk.scrolledtext.ScrolledText(self.leftframe)
      self.input.pack(padx = 5, pady=2, fill = "both", expand = True)

   def create_output_window(self):
      self.output = tk.scrolledtext.ScrolledText(self.rightframe, state = "disabled", cursor = "arrow")
      self.output.pack(padx = 5, pady = 2, fill = "both", expand = True)

   def create_console_window(self):
      self.console = tk.scrolledtext.ScrolledText(self.bottomframe, state = "disabled", cursor = "arrow", height = 6)
      self.console.pack(padx = 5, pady = 10, expand = True, fill = "x")

   def test_print(self):
      if(self.input.get("1.0","end-1c" ) == "hi"):
         self.output.config(state = "normal")
         self.output.insert(tk.INSERT, "hello ")
         self.output.config(state = "disabled")

   def interpreter_func(self):
      pass
   def save_load_func(self):
      pass


if __name__ == "__main__":
   root = tk.Tk()
   app = Application(master=root)
   app.mainloop()