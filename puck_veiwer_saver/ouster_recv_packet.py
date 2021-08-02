#!/usr/bin/env python
import multiprocessing
import socket
import numpy as np
import sys

def main():
    ## LIDAR data recv UDP setting
    print("ouster packet recv wating...")
    IP_ADDRESS = "192.168.0.118"
    PORT_NO = 7502
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((IP_ADDRESS, PORT_NO))
    ## python TCP send data setting
    s = serverSocket.recv(34896)
    print(s)
    # print(len(serverSocket.recv(34896)))
    with open("ouster_packet_1", "wb") as f:
        f.write(s)
    # while True: ## 실시간 관찰
    serverSocket.recv(34896)

    print("finish")
        # print(len(serverSocket.recv(24896)))
if __name__ == "__main__":
    main()