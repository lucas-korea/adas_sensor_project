# Import the required library
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Create an instance of tkinter frame
win=Tk()

# Set the geometry
win.geometry("700x350")

# Add a Scrollbar(horizontal)
h=Scrollbar(win, orient='horizontal')
h.pack(side=BOTTOM, fill='x')

# Add a text widget
text=Text(win, wrap=NONE, xscrollcommand=h.set)
text.pack()

# Add some text in the text widget
for i in range(5):
   text.insert(END, "Welcome to Tutorialspoint...")

# Attach the scrollbar with the text widget
h.config(command=text.xview)

win.mainloop()