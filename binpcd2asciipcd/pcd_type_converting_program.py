import os
import struct
from tkinter import *
import tkinter.ttk
from tkinter import filedialog
from tkinter import messagebox


def select_file(str_ = "파일을 선택 해주세요"):
    files = filedialog.askopenfilenames(initialdir=os.getcwd(),
                                        title=str_,
                                        filetypes=(("*.pcd", "*pcd"), ("*.txt", "*txt"), ("*.xls", "*xls"), ("*.csv", "*csv")))
    if files == '':
        print("파일을 추가 하세요")
        messagebox.showwarning("경고", "파일을 추가 하세요")  # 파일 선택 안했을 때 메세지 출력
        exit(1)
    dir_path = [0 for i in range(len(files))]
    file_list = [0 for i in range(len(files))]
    for i in range(len(files)):
        dir_path[i] = ("\\".join(list(files)[i].split("/")[: -1]))  # path 추출
        file_list[i] = ("\\".join(list(files)[i].split("/"))) #path\\파일명 추출
    return file_list, dir_path


def select_folder(str_ = "폴더를 선택해주세요"):
    folder = filedialog.askdirectory(initialdir=os.getcwd(),
                                        title=str_)
    if folder == '':
        print("폴더을 추가 하세요")
        messagebox.showwarning("경고", "폴더을 추가 하세요")  # 파일 선택 안했을 때 메세지 출력
        exit(1)
    return "\\".join(folder.split("/"))


def parsing_binPCD2asciiPCD(PCD, type_list, count_list):
    start = 0
    lines = [[]]

    pack_str = ""
    format_str = ""
    byte_len = 0
    type_list[-1] = type_list[-1].replace('\n', '')
    type_list[-1] = type_list[-1].replace('\r', '')
    for i in range(len(type_list)):
        if (type_list[i] == "F"):
            for j in range(int(count_list[i])):
                pack_str = pack_str + "f"
                format_str = format_str + "{:.6f} "
                byte_len = byte_len + 4
        elif (type_list[i] == "U"):
            for j in range(int(count_list[i])):
                pack_str = pack_str + "B"
                format_str = format_str + "{} "
                byte_len = byte_len + 1
    line_i = 0
    format_str = format_str.split(" ")
    while (1):
        try:
            scalar_fileds = struct.unpack(pack_str, PCD[start: start + byte_len])  # B:부호없는 정수, c:문자
            for i in range(len(type_list)):
                lines[line_i] = str(lines[line_i]) + " " + format_str[i].format(scalar_fileds[i])
            lines.append("")
            if line_i == 0:
                lines[line_i] = lines[line_i][3:]
            else :
                lines[line_i] = lines[line_i][1:]
            start = start + byte_len
            line_i = line_i + 1
        except Exception as e:
            break
    return lines


def binPCD2asciiPCD(file_list): # args가 없으면 코드가 위치한 디렉토리에서 검색,변환
    file_i = 0
    save_path = select_folder("저장할 폴더를 지정하세요")
    for file_name in file_list: #디렉토리 내 pcd 확장자 파일 대상으로 변환 시작 (ascii binary 구분없이 다 처리함)(근데 ascii 타입 pcd는 에러가 난다)
        file_i = file_i + 1
        print("{} / {} now converting file name : {}".format(file_i, len(file_list), file_name))
        Origin_pcd_f = open(file_name, 'rb')
        header = []
        field_list = []
        size_list = []
        type_list = []
        count_list = []
        breaker = False

        line = Origin_pcd_f.readline().decode()
        line = line.replace("\r", "")
        line = line.replace("\n", "")
        header.append(line+'\n')
        while line:
            line = Origin_pcd_f.readline().decode()
            line = line.replace("\r", "")
            line = line.replace("\n", "")
            words = line.split(' ')
            if words[0] == "DATA":
                if words[1] != "binary":
                    breaker = True
                    print("skip {} cause it is not bin type".format(file_name))
                    break
                header.append("DATA ascii\n")
                break
            elif words[0] == "FIELDS":
                for j in range(len(words)-1):
                    field_list.append(words[j+1])
            elif words[0] == "SIZE":
                for j in range(len(words)-1):
                    size_list.append(words[j+1])
            elif words[0] == "TYPE":
                for j in range(len(words)-1):
                    type_list.append(words[j+1])
            elif words[0] == "COUNT":
                for j in range(len(words)-1):
                    count_list.append(words[j+1])
            header.append(line+'\n')
        if breaker:
            continue
        PCD_data_part = Origin_pcd_f.read() # 헤더까지 다 읽은 기록이 있기 때문에, 나머지를 다 읽으면 PCD 데이터 부분이다.
        lines = parsing_binPCD2asciiPCD(PCD_data_part, type_list, count_list)
        with open (save_path + '\\' + file_name.split('\\')[-1][:-4] + "_ascii.pcd", 'w') as f:
            f.write(''.join(header))
            f.write('\n'.join(lines))
        Origin_pcd_f.close()


def asciiPCD2binPCD(file_list):
    file_i = 0
    save_path = select_folder("저장할 폴더를 지정하세요")
    for file_name in file_list:
        file_i = file_i + 1
        print("{} / {} now converting file name : {}".format(file_i, len(file_list), file_name))
        f = open(file_name, 'r')
        header = []
        list_pcd = []
        type_list = []
        count_list = []
        read_suc = []
        breaker = False
        while(1):
            try:
                line = f.readline()
                line = line.replace("\r", "")
                line = line.replace("\n", "")
            except Exception as e:
                print("skip {} cause {}".format(file_name,e))
                breaker = True
                break
            words = line.split(" ")
            if words[0] == "DATA":
                if words[1] != "ascii":
                    breaker = True
                    print("skip {} cause it is not ascii type".format(file_name))
                    break
                header.append("DATA binary\n")
                read_suc = f.readline()
                break
            elif words[0] == "TYPE":
                for j in range(len(words)-1):
                    type_list.append(words[j+1])
            elif words[0] == "COUNT":
                for j in range(len(words)-1):
                    count_list.append(words[j+1])
            header.append(line+'\n')
        if breaker:
            continue
        while read_suc:
            splited_line = read_suc.split(' ')
            for j in range(len(splited_line)):
                if j + 1  == len(splited_line):
                    splited_line[j] = splited_line[j].replace('\n', "")
                if type_list[j] == "F":
                    splited_line[j] = float(splited_line[j])
                elif type_list[j] == "U":
                    splited_line[j] = int(splited_line[j])
            list_pcd.append(splited_line)
            read_suc = f.readline()
        f.close()
        pack_str = ""
        for i in range(len(type_list)):
            if type_list[i] == "F":
                for j in range(int(count_list[i])):
                    pack_str = pack_str + "f"
            elif type_list[i] == "U":
                for j in range(int(count_list[i])):
                    pack_str = pack_str + "B"
        with open(save_path + '\\' + file_name.split('\\')[-1][:-4] + "_bin.pcd", 'w') as f:
            f.write(''.join(header))
        with open(save_path + file_name.split('\\')[-1][:-4] + "_bin.pcd", 'ab') as f:
            for j in range(len(list_pcd)):
                for k in range(len(pack_str)):
                    f.write(struct.pack(pack_str[k], list_pcd[j][k]))

global status
status = -1

def status1():
    global status
    status = 1

def status2():
    global status
    if status == 1:
        print('you have to check only one box')
    status = 2

def converting(event):
    if status == 1:
        print("asciiPCD2binPCD")
        file_list, path = select_file("asciiPCD2binPCD를 위한 파일들을 선택해주세요")
        asciiPCD2binPCD(file_list)
        print("done")
        exit(1)
    elif status == 2:
        print("binPCD2asciiPCD")
        file_list, path = select_file("binPCD2asciiPCD를 위한 파일들을 선택해주세요")
        binPCD2asciiPCD(file_list)
        print("done")
        exit(1)

if __name__ == "__main__":
    window = Tk()
    window.title("select converting type")

    CheckVar1 = IntVar()
    CheckVar2 = IntVar()

    c1 = Checkbutton(window, text="ascii2bin", variable=CheckVar1, command=status1)
    c2 = Checkbutton(window, text="bin2ascii", variable=CheckVar2, command=status2)

    c1.pack()
    c2.pack()

    save_btn = tkinter.Label(window, text="converting", bg='grey19', fg='snow')
    save_btn.bind('<Button-1>', converting)
    save_btn.place(x=170, y=50)

    window.geometry('400x100')
    window.mainloop()
