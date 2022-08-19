import cv2

src = cv2.imread('0706SignalImagenewJig_underlidar_outside.png', cv2.IMREAD_GRAYSCALE)

# 원본 이미지를 띄우고, 마우스 이벤트 처리도 도와줌
roi = cv2.selectROI(src)  # 원하는 부분(관심영역,  roi)을 선택하기
print('roi =', roi)  # (x 시작 지점, y 시작 지점, x축 드래그 한 길이, y축 드래그 한 길이)
# print(type(roi))    # <class 'tuple'>

img = src[roi[1]:roi[1] + roi[3],
      roi[0]:roi[0] + roi[2]]

# print(type(img))    # <class 'numpy.ndarray'>

# 원본 이미지인 img를 띄워주는 코드는 없음
# cv2.imshow('Img', img)  # 관심영역을 새 창으로 띄워주기
# cv2.rectangle(img=src, pt1=(0,0), pt2=(roi[2],roi[3]), color=(255,255,255))
# cv2.imshow('image', src)
cv2.waitKey()
cv2.destroyAllWindows()

img = cv2.imread('0706SignalImagenewJig_underlidar_outside.png')
cv2.imshow('img', img)
drag = False # drag 상태
defalut_x, default_y, w, h = -1,-1,-1,-1 # 좌표
blue = (255,0,0)
cv2.waitKey()
cv2.destroyAllWindows()

def Mouse(event, x, y, flag, param):
    global drag, default_x, default_y, img # global variance
    if event == cv2.EVENT_LBUTTONDOWN: # 왼쪽 버튼 누름
        drag = True
        default_x = x
        default_y = y
    elif event == cv2.EVENT_MOUSEMOVE: # 마우스 이동
        if drag:
            draw = img.copy() # img 복제
            cv2.rectangle(draw, (default_x, default_y), (x,y), blue, 3)
            cv2.imshow("img", draw)
    elif event == cv2.EVENT_LBUTTONUP: # 왼쪽 버튼 뗌
        if drag:
            drag = False
            w = x - default_x
            h = y - default_y
            if w > 0 and h > 0:
                draw = img.copy()
                cv2.rectangle(draw, (default_x, default_y), (x,y), blue, 3)
                cv2.imshow("img", draw)
                roi = img[default_y:default_y+h, default_x:default_x+w]
                cv2.imshow("drag", roi) # drag 한 창 생성
                cv2.imwrite('drag.jpg', roi) # drag 내용 저장
            else:
                cv2.imshow('img',img)

cv2.setMouseCallback('img', Mouse)
cv2.waitKey()
cv2.destroyAllWindows()