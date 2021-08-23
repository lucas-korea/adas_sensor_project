import os
import struct
from tkinter import filedialog
from tkinter import messagebox


def select_file():
    files = filedialog.askopenfilenames(initialdir=os.getcwd(),
                                        title="파일을 선택 해 주세요",
                                        filetypes=(("*.pcd", "*pcd"), ("*.txt", "*txt"), ("*.xls", "*xls"), ("*.csv", "*csv")))
    if files == '':
        messagebox.showwarning("경고", "파일을 추가 하세요")  # 파일 선택 안했을 때 메세지 출력
        exit(1)
    path = ("\\".join(list(files)[0].split("/")[0: -1]))  # lidar 데이터 목록 위치 추출
    return files, path


def asciiPCD2binPCD(file_list):
    for file_name in file_list:
        print(file_name)
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
            except Exception as e:
                print(e)
                breaker = True
                break
            words = line.split(" ")
            if words[0] == "DATA":
                if words[1][:5] != "ascii":
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
            header.append(line)
        if breaker:
            continue
        type_list[-1] = type_list[-1].replace('\n', '')
        type_list[-1] = type_list[-1].replace('\r', '')
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
        with open(file_name[:-4] + "_bin.pcd", 'w') as f:
            f.write(''.join(header))
        with open(file_name[:-4] + "_bin.pcd", 'ab') as f:
            for j in range(len(list_pcd)):
                for k in range(len(pack_str)):
                    f.write(struct.pack(pack_str[k], list_pcd[j][k]))


if __name__ == "__main__":
    file_list, path = select_file()
    asciiPCD2binPCD(file_list)
