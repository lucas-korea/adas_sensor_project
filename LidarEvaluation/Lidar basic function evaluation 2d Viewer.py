import cv2
import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from PIL import Image
from PIL import ImageTk
from functools import partial
import numpy as np
import PCD2PNG

BUTTONWORK = False


def draw_ROI( bbox_x1, bbox_y1, bbox_x2, bbox_y2, crop_x1, crop_x2, resize_ratio):
    global ref_png,range_png, RefLidarImage, RangeLidarImage
    if bbox_x1.get() == None or bbox_x2.get() == None or bbox_y1.get() == None or bbox_y2.get() == None:
        print("wrong bbox num, enter right digit")
    elif crop_x1.get() == None or crop_x2.get() == None:
        print("wrogn crop num, enter right number")

    bbox_x1 = int(bbox_x1.get())
    bbox_y1 = int(bbox_y1.get())
    bbox_x2 = int(bbox_x2.get())
    bbox_y2 = int(bbox_y2.get())
    crop_x1 = int(crop_x1.get())
    crop_x2 = int(crop_x2.get())
    resize_ratio = float(resize_ratio.get())

    ref_img = cv2.cvtColor(ref_png, cv2.COLOR_BGR2RGB)
    range_img = cv2.cvtColor(range_png, cv2.COLOR_BGR2RGB)
    Rangetext.delete("1.0", "end")
    Reftext.delete("1.0", "end")
    Ref_avg.delete("1.0", "end")
    Range_avg.delete("1.0", "end")
    # textbox에 bbox의 intensity, range를 적어넣기
    Ref_mean = 0
    Range_mean = 0
    for i in range(bbox_y2 - bbox_y1):
        for j in range(bbox_x2 - bbox_x1):
            Rangetext.insert(tkinter.CURRENT, '{0:6.3f}'.format(range_png_origin[bbox_y1+i,bbox_x1+j]))
            Rangetext.insert(tkinter.CURRENT, ' ')
            Reftext.insert(tkinter.CURRENT, '{0:6.3f}'.format(ref_png_origin[bbox_y1+i,bbox_x1+j]))
            Reftext.insert(tkinter.CURRENT, ' ')

            Range_mean += range_png_origin[bbox_y1 + i, bbox_x1 + j]
            Ref_mean += ref_png_origin[bbox_y1 + i, bbox_x1 + j]
        Rangetext.insert(tkinter.CURRENT, '\n')
        Reftext.insert(tkinter.CURRENT, '\n')
    Ref_avg.insert(tkinter.CURRENT, Ref_mean / ((bbox_y2 - bbox_y1)*(bbox_x2 - bbox_x1)))
    Range_avg.insert(tkinter.CURRENT, Range_mean / ((bbox_y2 - bbox_y1)*(bbox_x2 - bbox_x1)))

    RefROI = np.zeros((ref_img.shape[0], ref_img.shape[1], 3), dtype=np.uint8)
    RangeROI = np.zeros((range_img.shape[0], range_img.shape[1], 3), dtype=np.uint8)
    # crop image
    RefROI[0: ref_img.shape[0], crop_x1: crop_x2] = ref_img[0: ref_img.shape[0], crop_x1: crop_x2]
    RangeROI[0: range_img.shape[0], crop_x1: crop_x2] = range_img[0: range_img.shape[0], crop_x1: crop_x2]
    # draw ROI in image
    RefROI = cv2.rectangle(RefROI, (bbox_x1, bbox_y1), (bbox_x2,bbox_y2), (255,50,50), 1)
    RangeROI = cv2.rectangle(RangeROI, (bbox_x1, bbox_y1), (bbox_x2,bbox_y2), (255,50,50), 1)
    # resize
    RefROI = cv2.resize(RefROI, (0,0), fx=resize_ratio, fy=resize_ratio)
    RangeROI = cv2.resize(RangeROI, (0,0), fx=resize_ratio, fy=resize_ratio)

    Ref_output_img = Image.fromarray(RefROI)
    Ref_imgtk = ImageTk.PhotoImage(image=Ref_output_img)
    RefLidarImage.config(image=Ref_imgtk)
    RefLidarImage.image = Ref_imgtk

    Range_output_img = Image.fromarray(RangeROI)
    Range_imgtk = ImageTk.PhotoImage(image=Range_output_img)
    RangeLidarImage.config(image=Range_imgtk)
    RangeLidarImage.image = Range_imgtk

# 이미지 원상복구
def RestoreImg():
    RefLidarImage.config(image=ref_imgtk)
    RefLidarImage.image = ref_imgtk
    RangeLidarImage.config(image=range_imgtk)
    RangeLidarImage.image = range_imgtk
    Reftext.delete("1.0", "end")
    Rangetext.delete("1.0", "end")


range_png, ref_png = PCD2PNG.MakePCDimg("C:\\Users\\jcy37\\PycharmProjects\\LidarEvaluation\\20220802_110747_000001_821092_H_upper.pcd")

window=tkinter.Tk()
window.title("Katech Lidar evatluion program")
window.geometry(str(range_png.shape[1]+100) + "x800")

ref_png_origin = ref_png.copy()
ref_png = cv2.applyColorMap(ref_png, cv2.COLORMAP_JET)
ref_img = cv2.cvtColor(ref_png, cv2.COLOR_BGR2RGB)
ref_img = Image.fromarray(ref_img) #cv2 포맷을 tkinter가 읽을 수 있는 포맷으로 바꿔주는것으로 보인다.
ref_imgtk = ImageTk.PhotoImage(image=ref_img)
RefLidarImage = tkinter.Label(window, image=ref_imgtk)
RefLidarImage.place(x=0,y=0)
tkinter.Label(window, text="intensity").place(x=range_png.shape[1]+20,y=60)

range_png_origin = range_png.copy()
range_png = cv2.applyColorMap(range_png, cv2.COLORMAP_JET)
range_img = cv2.cvtColor(range_png, cv2.COLOR_BGR2RGB)
range_img = Image.fromarray(range_img) #cv2 포맷을 tkinter가 읽을 수 있는 포맷으로 바꿔주는것으로 보인다.
range_imgtk = ImageTk.PhotoImage(image=range_img)
RangeLidarImage = tkinter.Label(window, image=range_imgtk)
RangeLidarImage.place(x=0,y=128)
tkinter.Label(window, text="range").place(x=range_png.shape[1]+20,y=180)



# ROI 영역 선택
x1 = tkinter.StringVar()
y1 = tkinter.StringVar()
x2 = tkinter.StringVar()
y2 = tkinter.StringVar()
x1.set("10")
y1.set("10")
x2.set("20")
y2.set("20")
bbox_x1_lb = tkinter.Label(window, text="bbox x1").place(x=0,y=170+128)
bbox_x2_lb = tkinter.Label(window, text="bbox x2").place(x=0,y=190+128)
bbox_y1_lb = tkinter.Label(window, text="bbox y1").place(x=260,y=170+128)
bbox_y2_lb = tkinter.Label(window, text="bbox y2").place(x=260,y=190+128)
tkinter.Entry(window, textvariable=x1).place(x=50,y=170+128)
tkinter.Entry(window, textvariable=x2).place(x=50,y=190+128)
tkinter.Entry(window, textvariable=y1).place(x=310,y=170+128)
tkinter.Entry(window, textvariable=y2).place(x=310,y=190+128)

crop_num1 = tkinter.StringVar()
crop_num2 = tkinter.StringVar()
crop_num1.set("0")
crop_num2.set(str(range_png.shape[1]))
crop_x1_lb = tkinter.Label(window, text="crop x1").place(x=0,y=210+128)
crop_x2_lb = tkinter.Label(window, text="crop x2").place(x=260,y=210+128)
tkinter.Entry(window, textvariable=crop_num1).place(x=50,y=210+128)
tkinter.Entry(window, textvariable=crop_num2).place(x=310,y=210+128)

resize_ratio = tkinter.StringVar()
resize_ratio.set('1')
resize_ratio_lb = tkinter.Label(window, text="resize ratio").place(x=0, y=230+128)
tkinter.Entry(window, textvariable=resize_ratio).place(x=70,y=230+128)


draw_ROI = partial(draw_ROI,x1,y1,x2,y2, crop_num1, crop_num2, resize_ratio)
button = tkinter.Button(window, text="영역그리기", command=draw_ROI)
button.place(x=130,y=270+128)

# 원상 복구 button
button = tkinter.Button(window, text="원상복구", command=RestoreImg)
button.place(x=210,y=270+128)

# 선택된 ROI 에서 거리, intensity 보여주기
Ref_avg = tkinter.Text(height=1, width=10)
Ref_avg.place(x=600,y=270)
Ref_avg.insert(tkinter.CURRENT, '평균 값')

Range_avg = tkinter.Text(height=1, width=10)
Range_avg.place(x=600,y=520)
Range_avg.insert(tkinter.CURRENT, '평균 거리')

tkinter.Label(window, text="intensity").place(x=500,y=270)
Reftext = tkinter.Text(height=15, width=70, wrap=NONE)
Reftext.place(x=500,y=300)
Reftext_vertical_scroll = tkinter.Scrollbar(window, orient='vertical', command=Reftext.yview)
Reftext_vertical_scroll.place(x=1000,y=300, height=200)
Reftext_horizontal_scroll = tkinter.Scrollbar(window, orient="horizontal", command=Reftext.xview)
Reftext_horizontal_scroll.place(x=500, y=500, width = 400)
Reftext.config(yscrollcommand=Reftext_vertical_scroll.set, xscrollcommand=Reftext_horizontal_scroll.set)

tkinter.Label(window, text="Range").place(x=500,y=520)
Rangetext = tkinter.Text(height=15, width=70, wrap=NONE)
Rangetext.place(x=500,y=550)
Rangetext_vertical_scroll = tkinter.Scrollbar(window, orient='vertical', command=Rangetext.yview)
Rangetext_vertical_scroll.place(x=1000,y=550, height=200)
Rangetext_horizontal_scroll = tkinter.Scrollbar(window, orient="horizontal", command=Rangetext.xview)
Rangetext_horizontal_scroll.place(x=500, y=750, width = 400)
Rangetext.config(yscrollcommand=Rangetext_vertical_scroll.set, xscrollcommand=Rangetext_horizontal_scroll.set)


window.mainloop()