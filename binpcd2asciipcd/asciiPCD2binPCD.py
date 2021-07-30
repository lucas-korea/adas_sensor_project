import sys
import numpy as np
import os
import struct

def asciiPCD2binPCD(file_list):
    for file_name in file_list:
        print(file_name)
        f = open(file_name, 'r')
        header = []
        list_pcd = []
        field_list = []
        size_list = []
        type_list = []
        count_list = []
        for i in range(15):
            line = f.readline()
            words = line.split(" ")
            if words[0] == "DATA":
                header.append("DATA binary\n")
                read_suc = f.readline()
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
            header.append(line)
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
            if (type_list[i] == "F"):
                for j in range(int(count_list[i])):
                    pack_str = pack_str + "f"
            elif (type_list[i] == "U"):
                for j in range(int(count_list[i])):
                    pack_str = pack_str + "B"
        with open(file_name[:-4] + "_bin.pcd", 'w') as f:
            f.write(''.join(header))
        with open(file_name[:-4] + "_bin.pcd", 'ab') as f:
            for j in range(len(list_pcd)):
                for k in range(len(pack_str)):
                    f.write(struct.pack(pack_str[k], list_pcd[j][k]))
        exit(1)

if __name__ == "__main__":
    file_list = os.listdir(os.getcwd())
    file_list = [file for file in file_list if file.startswith("2_")]  ## 지정된 디렉토리 내 pcd 파일만 검색
    file_list = [file for file in file_list if not file.endswith("bin.pcd")]
    asciiPCD2binPCD(file_list)