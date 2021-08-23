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


def parsing_PCD_data(PCD, type_list, count_list):
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
            print(e)
            print("end of pcd file")
            break
    return lines


def parsing_bin_PCD(file_list): # args가 없으면 코드가 위치한 디렉토리에서 검색,변환
    for file_name in file_list: #디렉토리 내 pcd 확장자 파일 대상으로 변환 시작 (ascii binary 구분없이 다 처리함)(근데 ascii 타입 pcd는 에러가 난다)
        print("now converting file name :" , file_name)
        Origin_pcd_f = open(file_name, 'rb')
        field_list = []
        size_list = []
        type_list = []
        count_list = []
        header = []

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
        PCD_data_part = Origin_pcd_f.read() # 헤더까지 다 읽은 기록이 있기 때문에, 나머지를 다 읽으면 PCD 데이터 부분이다.
        lines = parsing_PCD_data(PCD_data_part, type_list, count_list)
        with open (file_name[:-4] + "_ascii.pcd", 'w') as f:
            f.write(''.join(header))
            f.write('\n'.join(lines))
        Origin_pcd_f.close()


if __name__ == "__main__":
    file_list, path = select_file()
    parsing_bin_PCD(file_list)
