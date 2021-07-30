from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk

def main():
    global select_return
    select_return = 0
    root = Tk()
    root.title("Downloader")
    root.geometry("800x200")

    root.filename = filedialog.askopenfiles()
    def btncmd():
        print(select_return)

    btn = Button(root, text="변환", command=btncmd)
    btn.pack()

    def select():
        global select_return
        select_return = r.get()

    r = IntVar()


    r1 = Radiobutton(root, text = "ascii2pcd", variable=r, value="1", command=select)
    r1.pack(anchor = W)

    r2 = Radiobutton(root, text = "bin2ascii", variable=r, value="2", command=select)
    r2.pack(anchor = W)

    show = Label(root)
    show.pack()


    text = Text(root)
    for i in range(len(root.filename)):
        text.insert(CURRENT, str(root.filename[i].name)+"\n")
    text.pack()

    root.mainloop()

if __name__ == "__main__":
    main()