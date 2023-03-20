from tkinter import *
import random

def set_color(serve):
   if serve:
      root.configure(background = ['green'])
   else:
      root.configure(background = ['red'])

SERVE = 0

root = Tk()
root.title("Serve In or Out")
root.resizable(False, False)
root.attributes("-fullscreen", True)
# root.attributes('-zoomed', True)
# w, h = root.winfo_screenwidth(), root.winfo_screenheight()
# root.geometry("%dx%d+0+0" % (w, h))

set_color(SERVE)

root.mainloop()