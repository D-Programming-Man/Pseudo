import tkinter as tk
from guilib.application import Application
from interpreter import interpret
import sys

if __name__ == "__main__":
   root = tk.Tk()
   app = Application(master=root)
   
   # When user presses the X button to close GUI
   def close():
      sys.exit(0)
   root.protocol("WM_DELETE_WINDOW", close)
   
   app.mainloop()
