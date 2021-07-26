import multiprocessing
from multiprocessing import Process, Queue


def work(id, start, end, result):
    total = 0
    for i in range(start, end):
        total += 1
    result.put(total)
    return


if __name__ == "__main__":
    START, END = 0, 100000
    result = Queue()
    th1 = Process(target=work, args=(1, START, END // 2, result))
    th2 = Process(target=work, args=(2, END // 2, END, result))
    th3 = Process(target=work, args=(1, START, END // 2, result))
    th4 = Process(target=work, args=(2, END // 2, END * 100, result))
    while True:

        th1.start()
        th2.start()
        th3.start()
        th4.start()
        th1.join()
        # th2.join()



        result.put('STOP')
        total = 0
        print(result)
        while True:
            tmp = result.get()
            print(tmp)
            if tmp == 'STOP':
                break
            else:
                total += tmp
        print(f"Result: {total}")
        th4.join()
        print("here")
        print(result.get())
        print("here2")