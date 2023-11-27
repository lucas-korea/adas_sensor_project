file_path = "E:\\공주대 샘플 데이터(실내촬영, 2minute)\\20230818_142349\\Frame_TimeStamp_20230818_142349.bin"
with open(file_path, "rb") as f:
    data = f.readlines()
    timestamp_arr = []
    for lnie in data:
        timestamp = lnie.decode().split('\t')[-1]
        timestamp_arr.append(int(timestamp))

    interval = []
    for i in range(len(timestamp_arr)-1):
        inter = timestamp_arr[i+1] - timestamp_arr[i]
        interval.append(inter)
        if inter > 36 or inter <30:
            print("warn", i)
            print(timestamp_arr[i+1], timestamp_arr[i])
    print(interval)


# match = open(file_path, encoding='utf8')
# lines = match.readlines()
# print(lines)