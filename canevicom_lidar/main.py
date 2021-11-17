import multiprocessing
import socket
import parse
import numpy as np

LIDAR_DATA_BYTES = 1855521

def get_data_PCL(serverSocket_):
    count = 0
    while True:
        count += 1
        ## 라이다 데이터 패킷을 메뉴얼에 따라 파싱하여 리턴하는 함수
        get_data, point_cloud = parse.parse_pos(serverSocket_.recv(1206), count)
        if (get_data):
            break
    return point_cloud

def main():
    ## LIDAR data recv UDP setting
    IP_ADDRESS = "192.168.100.13"
    PORT_NO = 5001
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(serverSocket.bind((IP_ADDRESS, PORT_NO)))
    a = serverSocket.recv(1480)
    print(a)


if __name__ == "__main__":
    main()