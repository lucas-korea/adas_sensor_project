import cv2
import tkinter
from tkinter import ttk
# from tkinter import *
from PIL import Image
from PIL import ImageTk
from functools import partial
import numpy as np

GREYcheck = False
DRAWRIO = False
CROPROI = False

def crop_ROI( x1_, x2_):
    global ref_png, RefLidarImage, CROPROI
    if x1_.get() == None or x2_.get() == None:
        print("wrong num, enter right digit")
        return
    if CROPROI == False:
        img = cv2.cvtColor(ref_png, cv2.COLOR_BGR2RGB)
        ROI = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
        ROI[0 : img.shape[0], int(x1_.get()) : int(x2_.get())] = img[0 : img.shape[0], int(x1_.get()) : int(x2_.get())]
        img = Image.fromarray(ROI)
        imgtk = ImageTk.PhotoImage(image=img)

        RefLidarImage.config(image=imgtk)
        RefLidarImage.image = imgtk
        # CROPROI=True


def draw_ROI( x1_, y1_, x2_, y2_):
    global ref_png, RefLidarImage, DRAWRIO
    if x1_.get() == None or x2_.get() == None or y1_.get() == None or y2_.get() == None:
        print("wrong num, enter right digit")
        return

    if DRAWRIO == False:
        img = cv2.cvtColor(ref_png, cv2.COLOR_BGR2RGB)
        for i in range(int(y2_.get()) - int(y1_.get())):
            for j in range((int(x2_.get()) - int(x1_.get()))):
                Rangetext.insert(tkinter.CURRENT, (img[int(x1_.get())+j, int(x1_.get())+i][0]-img[int(x1_.get())+j, int(x1_.get())+i][2]+255)/2)
                Rangetext.insert(tkinter.CURRENT, ' ')
            Rangetext.insert(tkinter.CURRENT, '\n')

        ROI = cv2.rectangle(img, (int(x1_.get()), int(y1_.get())), (int(x2_.get()),int(y2_.get())), (255,100,100), 2)
        img = Image.fromarray(ROI)
        imgtk = ImageTk.PhotoImage(image=img)

        RefLidarImage.config(image=imgtk)
        RefLidarImage.image = imgtk

        DRAWRIO=True
    else:
        img = cv2.cvtColor(ref_png, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)

        RefLidarImage.config(image=imgtk)
        RefLidarImage.image = imgtk
        Rangetext.delete("1.0", "end")
        DRAWRIO=False


window=tkinter.Tk()
window.title("YUN DAE HEE")
window.geometry("2240x800")

ref_png = cv2.imread("C:\\Users\\jcy37\\PycharmProjects\\LidarEvaluation\\0706RefimageoldJig_underlidar_outside2.png")
ref_png_origin = ref_png.copy()
ref_img = cv2.cvtColor(ref_png, cv2.COLOR_BGR2RGB)
ref_img = Image.fromarray(ref_img) #cv2 포맷을 tkinter가 읽을 수 있는 포맷으로 바꿔주는것으로 보인다.
ref_imgtk = ImageTk.PhotoImage(image=ref_img)
RefLidarImage = tkinter.Label(window, image=ref_imgtk)
RefLidarImage.place(x=0,y=0)

range_png = cv2.imread("C:\\Users\\jcy37\\PycharmProjects\\LidarEvaluation\\0706RangeImageoldJig_underlidar_outside1.png")
range_png_origin = ref_png.copy()
range_img = cv2.cvtColor(range_png, cv2.COLOR_BGR2RGB)
range_img = Image.fromarray(range_img) #cv2 포맷을 tkinter가 읽을 수 있는 포맷으로 바꿔주는것으로 보인다.
range_imgtk = ImageTk.PhotoImage(image=range_img)
RangeLidarImage = tkinter.Label(window, image=range_imgtk)
RangeLidarImage.place(x=0,y=128)

# ROI 영역 선택
x1 = tkinter.StringVar()
y1 = tkinter.StringVar()
x2 = tkinter.StringVar()
y2 = tkinter.StringVar()
x1.set("10")
y1.set("10")
x2.set("20")
y2.set("20")
lb1 = tkinter.Label(window, text="x1y1").place(x=0,y=170+128)
lb2 = tkinter.Label(window, text="x2y2").place(x=0,y=190+128)
tkinter.Entry(window, textvariable=x1).place(x=40,y=170+128)
tkinter.Entry(window, textvariable=y1).place(x=300,y=170+128)
tkinter.Entry(window, textvariable=x2).place(x=40,y=190+128)
tkinter.Entry(window, textvariable=y2).place(x=300,y=190+128)
draw_ROI = partial(draw_ROI,x1,y1,x2,y2)
button = tkinter.Button(window, text="영역그리기", command=draw_ROI)
button.place(x=150,y=220+128)

#특정 영역 crop
crop_num1 = tkinter.StringVar()
crop_num2 = tkinter.StringVar()
crop_num1.set("0")
crop_num2.set("360")
lb3 = tkinter.Label(window, text="x1x2").place(x=0,y=250+128)
tkinter.Entry(window, textvariable=crop_num1).place(x=40,y=250+128)
tkinter.Entry(window, textvariable=crop_num2).place(x=300,y=250+128)
crop_ROI = partial(crop_ROI,crop_num1, crop_num2)
button = tkinter.Button(window, text="특정 영역 크롭", command=crop_ROI)
button.place(x=150,y=280+128)

# 선택된 ROI 에서 거리, intensity 보여주기
avg_ref = tkinter.Text(window)
avg_ref.insert(tkinter.CURRENT, '평균 값')

avg_range = tkinter.Text(window)
avg_range.insert(tkinter.CURRENT, '평균 거리')

Rangetext = tkinter.Text(height=20, width=100)
Rangetext.place(x=500,y=400)
vsb = tkinter.Scrollbar(window)
vsb.place(x=1250,y=400)
vsb.config(command=Rangetext.yview)
vsb2 = tkinter.Scrollbar(window)
vsb2.place(x=500, y=700)
vsb2.config(orient="horizontal", command=Rangetext.xview)
Rangetext.config(yscrollcommand=vsb.set, xscrollcommand=vsb2.set)

window.mainloop()