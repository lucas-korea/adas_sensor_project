from tkinter import *
import cv2
import pyautogui
import numpy as np
import threading
from tkinter import messagebox as msgbox
from tkinter import filedialog

# 함수 정의 1.녹화 함수
run = False  # 버튼 누르면 종료 명령


def record():
    global file_name_entry, save_dir_entry
    resolution = (1920, 1080)  # 화면 해상도
    codec = cv2.VideoWriter_fourcc(*'XVID')  # 비디오 코덱 설정
    filename = '{}.avi'.format(file_name_entry.get())  # 타이핑한 파일 이름 가져오기
    location = save_dir_entry.get()  # 입력한 저장경로 가져오기
    fps = 10.0
    out = cv2.VideoWriter(location + '/' + filename, codec, fps, resolution)  # 결과물

    while True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)

        if run == False:  # run 변수가 거짓이 되면 프로그램 종료
            break

    out.release()
    cv2.destroyAllWindows()


recording = False  # 시작에는 녹화 중이 아님


# 함수 정의 2: 버튼 누르면 작동할 함수
def record_startstop():  # 녹화상태를 바꿔주고, 녹화상태면 스레드를 실행시켜주는 함수
    global recording, run
    recording = not recording  # 실행시키면 recording 상태가 변해야 함

    if save_dir_entry.get() == '':
        msgbox.showerror('경고', '저장 경로를 설정해주세요.')  # 저장경로 엔트리가 비었으면 에러메세지
        recording = not recording  # 녹화 상태는 변해서는 안 되니깐
    elif file_name_entry.get() == '':
        msgbox.showerror('경고', '파일 이름을 저장해주세요.')  # 파일이름 엔트리가 비었으면 에러메세지

    elif recording:
        run = True
        msgbox.showinfo('알림', '녹화를 시작합니다.')
        btn_stop.config(state='active')  # 녹화 중지버튼 활성화
        btn_start.config(state='disabled')  # 녹화 시작버튼 비활성화
        thread = threading.Thread(target=record)  # 스레드 설정부터 시작
        thread.setDaemon(True)
        thread.start()

    elif recording == False:
        run = False  # 프로그램 종료를 위한 값
        btn_start.config(state='active')  # 이때만 저장공간 엔트리는 작동 가능하게 바꾸기
        btn_stop.config(state='disabled')
        msgbox.showinfo('알림', '녹화가 완료되었습니다.')


def save_dir():
    folder_selected = filedialog.askdirectory()  # 디렉토리 찾는 창 띄우기
    if folder_selected == '':
        return  # 선택된 폴더가 없으면 돌아가기
    save_dir_entry.config(state='normal')
    save_dir_entry.delete(0, END)  # 저장경로 엔트리 우선 비우고
    save_dir_entry.insert(0, folder_selected)  # 선택된 폴더 주소를 삽입
    save_dir_entry.config(state='normal')


# 기본적인 화면 세팅
root = Tk()
root.title('화면 녹화')
root.resizable(False, False)

# 녹화 시작, 중지 버튼 프레임
btn_frame = Frame(root)
btn_frame.pack(fill='x', pady=5, padx=5)
# 녹화 시작, 중지 버튼
btn_start = Button(btn_frame, text='녹화 시작', width=10, command=record_startstop)
btn_start.pack(side='left', padx=5, pady=5, expand=True)
btn_stop = Button(btn_frame, text='녹화 중지', width=10, command=record_startstop)
btn_stop.pack(side='right', padx=5, pady=5, expand=True)

# 저장 경로 프레임
save_dir_frame = LabelFrame(root, text='저장 경로')
save_dir_frame.pack(padx=5, pady=5, fill='x')
# 저장경로 찾아보기 버튼
btn_save_dir = Button(save_dir_frame, text='찾아보기..', width=10, command=save_dir)
btn_save_dir.pack(padx=5, pady=5, side='left')
# 저장경로 엔트리
save_dir_entry = Entry(save_dir_frame, state='readonly')  # 저장공간 입력 불가능하게 만들기
save_dir_entry.pack(side='right', fill='x', padx=5, pady=5)

# 파일명 프레임
file_name_frame = Frame(root)
file_name_frame.pack(padx=5, pady=5, fill='x')
# 파일명 입력창과 설명칸
file_name_label = Label(file_name_frame, text='저장할 파일명 : ')
file_name_label.pack(side='left')
file_name_entry = Entry(file_name_frame)
file_name_entry.pack(padx=5, pady=5, fill='x')

root.mainloop()