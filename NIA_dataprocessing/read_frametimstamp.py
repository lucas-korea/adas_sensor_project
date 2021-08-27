with open("D:\\210826_test_sw4\\20210826_132604\\20210826_132812\\Frame_TimeStamp_20210826_132812.bin", 'r') as f:
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split("\t")[1].replace(' ','').replace('\n', '') + '_' + str(i) + '\n'
with open("D:\\210826_test_sw4\\20210826_132604\\20210826_132812\\Frame_TimeStamp_20210826_132812_.bin", 'w') as f:
    f.writelines(lines)