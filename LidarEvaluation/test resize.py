from tkinter import *

import PIL

from PIL import ImageTk, Image

root = Tk()

image = Image.open("images/2.png")

height = 500

width = 500

canvas = Canvas(root, height=500, width=500)

image = image.resize((height, width), PIL.Image.ANTIALIAS)

# if 0:   <- 화면의 height와 이미지의 heigt에 비례하면 이미지 width를 구한 후 이미지를 resize하는 경우

wpercent = (height / float(image.size[0]))

hsize = int((float(image.size[1]) * float(wpercent)))

image = image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)

# endif

photo = ImageTk.PhotoImage(image)

item4 = canvas.create_image(height / 2, width / 2, image=photo) < - 화면


canvas.pack(side=TOP, expand=True, fill=BOTH) < - 화면에

root.mainloop()