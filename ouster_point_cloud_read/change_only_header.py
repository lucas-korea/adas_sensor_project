import os

def main():
    file_list = []
    for root, dirs, files in os.walk('C:\\Users\\정찬영\\PycharmProjects\\ouster_point_cloud_read'):
        for fname in files:
            full_fname = os.path.join(root, fname)
            file_list.append(full_fname)
    file_list = [file for file in file_list if file.endswith(".pcd")]
    file_list = os.listdir(os.getcwd())
    file_list = [file for file in file_list if file.endswith(".pcd")]
    for file in file_list:
        replace_in_file(file)


def replace_in_file(file_path):
    print(file_path)
    fr = open(file_path, 'rb')
    header_lines = [0 for i in range(11)]
    for i in range(11):
        header_lines[i] = fr.readline().decode()
    data_lines = fr.read()
    fr.close()

    header_lines[10] = "DATA binary"
    with open(file_path, 'w') as f:
        for i in range(11):
            header_lines[i] = header_lines[i].replace("\r", "")
            header_lines[i] = header_lines[i].replace("\n", "")
            f.write(header_lines[i])
            f.write('\n')
    with open(file_path, 'ab') as f:
        f.write(data_lines)


if __name__ == '__main__':
    main()
