import serial
import threading
import time

port = "COM7"  # PC에 연결된 포트명
baud = 115200  # 시리얼 보드레이트(통신속도)
ser = serial.Serial(port, baud, timeout=1)


def main():
    thread = threading.Thread(target=readthread, args=(ser,))  # 시리얼 통신 받는 부분
    thread.start()

    # while True:
    #     data = '보낼데이터(byte형식으로 보내야함 byte,str.encode())'
    #     ser.write(data)
    #     time.sleep(1)


def readthread(ser):  # 데이터 받는 함수
    # 쓰레드 종료될때까지 계속 돌림
    while True:  # True 조건일대 쓰레드가 실행(원하는 조건문 변환해서 쓰세여)
        if ser.readable():  # 값이 들어왔는지 확인
            res = ser.readline()  # 값을 줄로 받음(byte형식)
            print(res)  # byte형식

    ser.close()


main()  # 메인문 실행