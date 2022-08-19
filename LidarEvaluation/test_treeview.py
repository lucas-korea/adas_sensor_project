from tkinter import ttk
import tkinter as tk

win = tk.Tk()
win.minsize(width=500, height=400)
win.resizable(width=0, height=0)

tree = ttk.Treeview(win, selectmode='extended')
tree.place(x=30, y=95)

vsb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
vsb.place(x=350, y=95, height=200+20)
vsb2 = ttk.Scrollbar(win, orient="horizontal", command=tree.xview)
vsb2.place(x=100, y=350, width=200)

tree.configure(yscrollcommand=vsb.set, xscrollcommand=vsb2.set)

tree["columns"] = ("1", "2", "3")
tree['show'] = 'headings'
tree.column("1", width=20, anchor='c')
tree.column("2", width=20, anchor='c')
tree.column("3", width=20, anchor='c')

tree.heading("1", text="Account")
tree.heading("2", text="Type")
tree.heading("3", text="Type2")

tree.insert("",'end',text="L1",values=("Big1","Best", "2"))
tree.insert("",'end',text="L2",values=("Big2","Best", "2"))
tree.insert("",'end',text="L3",values=("Big3","Best", "2"))
tree.insert("",'end',text="L4",values=("Big4","Best", "2"))
tree.insert("",'end',text="L5",values=("Big5","Best", "2"))
tree.insert("",'end',text="L6",values=("Big6","Best", "2"))
tree.insert("",'end',text="L7",values=("Big7","Best", "2"))
tree.insert("",'end',text="L8",values=("Big8","Best", "2"))
tree.insert("",'end',text="L9",values=("Big9","Best", "2"))
tree.insert("",'end',text="L10",values=("Big10","Best", "2"))
tree.insert("",'end',text="L11",values=("Big11","Best", "2"))
tree.insert("",'end',text="L15",values=("Big12","Best", "2"))
tree.update()
tree.column("1", width=100, anchor='c')
tree.column("2", width=100, anchor='c')
tree.column("3", width=100, anchor='c')

win.mainloop()