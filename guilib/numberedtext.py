import tkinter as tk

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None
        self.font = "Courier"
        self.fill = "black"
        self.fontsize = 10

    def attach(self, text_widget):
        self.textwidget = text_widget

    def setFont(self, name, size):
        self.font = name
        self.fontsize = size

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")
        
        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum, font=(self.font, self.fontsize), fill = self.fill)
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

    '''
    highlighter
    call the method on a customtext or class derived from customtext
    it will highlight every word in the keywords dict with the tag assigned to it
    current tags are: keyword, datatype, string
    '''

    def highlighter(self):

      keywords = {"Variable": "datatype", "Number": "datatype", "Int ": "datatype", "Int)": "datatype",
                  "Int,": "datatype", "String": "datatype", "str": "datatype", "List": "datatype",
                  "Table": "datatype", "dict": "datatype", "Function": "datatype", "Object": "datatype",

                  "Create ": "keyword", "Display ": "keyword", "Add ": "keyword", "Subtract ": "keyword",
                  "Multiply ": "keyword", "Divide ": "keyword", "Store ": "keyword", "Print": "keyword",
                  "Define ": "keyword", "def ": "keyword", "Run ": "keyword", "If": "keyword", "Loop": "keyword",
                  "for": "keyword", "Compare": "keyword", "While": "keyword", "Pycode": "keyword", "%": "keyword",
                  "Import": "keyword",

                  '"': "string", "'": "string", "#": "string"}



      for kw in keywords:

        start = self.index("1.0")
        end = self.index(tk.END)
        self.mark_set("kw_start", start)
        self.mark_set("kw_finish", start)
        self.mark_set("comment_blk", start)
        self.mark_set("limit", end)

        count = tk.IntVar()
        while True:
          index = self.search(kw, "kw_finish", "limit", count=count, regexp=False, nocase=True)
          if index == "":
            break
          if count.get() == 0:
            break
          self.mark_set("kw_start", index)

          if kw == "'" or kw == '"':

            self.mark_set("comment_blk", "%s+%sc" % (index, count.get()))
            next_index = self.search(kw, "comment_blk", "limit", count=count, regexp=True, nocase=True)

            if next_index == "":
              break
            if count.get() == 0:
              break

            if int(float(next_index)) > int(float(index)):
              self.mark_set("kw_finish", "%s+%sc" % (index, count.get()))
            else:
              self.mark_set("kw_finish", "%s+%sc" % (next_index, count.get()))

          elif kw == "#" or kw == "%" or kw == "Pycode":

            self.mark_set("comment_blk", "%s+%sc" % (index, count.get()))
            index = self.search("\n", "comment_blk", "limit", count=count, regexp=True, nocase=True)
            if index == "":
                break
            if count.get() == 0:
                break
            self.mark_set("kw_finish", "%s+%sc" % (index, count.get()))

          elif kw[-1] == ")" or kw[-1] == ",":
            self.mark_set("kw_finish", "%s+%sc-%sc" % (index, count.get(), "1"))

          else:
            self.mark_set("kw_finish", "%s+%sc" % (index, count.get()))

          self.tag_add(keywords[kw], "kw_start", "kw_finish")


class NumberedText(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.configure(bd = 0)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="right", fill="both", expand=True)
        self.linenumbers.pack(side="left", fill="y")

        self.text.tag_configure("keyword", foreground="red")
        self.text.tag_configure("datatype", foreground="blue")
        self.text.tag_configure("string", foreground="green")

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)
        
        self.has_changed = False

    def _on_change(self, event):
        self.linenumbers.redraw()
        self.has_changed = True

