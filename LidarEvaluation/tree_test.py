import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

columns = [f'Column {i}' for i in range(10)]

x_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
x_scrollbar.grid(row=1, column=0, sticky=tk.E+tk.W)
y_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
y_scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)

tree = ttk.Treeview(root, columns=columns, height=10, show="headings",
    xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
tree.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

for col in tree['columns']:
        tree.heading(col, text=f"{col}", anchor=tk.CENTER)
        tree.column(col, anchor=tk.CENTER, width=100)

for i in range(100):
    tree.insert('', 'end', values=[i*10+j for j in range(len(columns))])

x_scrollbar['command'] = tree.xview
y_scrollbar['command'] = tree.yview

root.mainloop()