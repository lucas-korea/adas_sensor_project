#!/usr/bin/env python
import multiprocessing
import socket
import parse
import numpy as np
import sys

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
    pool = multiprocessing.Pool(2)
    ## LIDAR data recv UDP setting
    IP_ADDRESS = "192.168.1.77"
    PORT_NO = 2368
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((IP_ADDRESS, PORT_NO))
    ## python TCP send data setting
    LOCALHOST = "127.0.0.1"
    PORT_NO2 = 999
    TCPserverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPserverSocket.bind((LOCALHOST, PORT_NO2))
    print("waiting...\n")
    TCPserverSocket.listen()
    clientSocket, addr = TCPserverSocket.accept()
    print("connected by", addr, "\nStart")
    while True: ## 실시간 관찰
        point_cloud = get_data_PCL(serverSocket)
        point_cloud = np.ndarray.tobytes(point_cloud)
        # if (sys.getsizeof(point_cloud) == LIDAR_DATA_BYTES):
        clientSocket.send(point_cloud)
        parse.clear_append_data()

if __name__ == "__main__":
    main()