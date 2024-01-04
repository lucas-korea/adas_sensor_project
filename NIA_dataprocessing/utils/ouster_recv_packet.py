#!/usr/bin/env python
import multiprocessing
import socket
import numpy as np
import sys

def main():
    ## LIDAR data recv UDP setting
    print("ouster packet recv wating...")
    IP_ADDRESS = "169.254.53.112"
    PORT_NO = 7502
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((IP_ADDRESS, PORT_NO))
    ## python TCP send data setting

    start = 700
    for i in range(start, start + 64):
        with open("data\\ouster_packet_" + str(i), "wb") as f:
            s = serverSocket.recv(24896)
            f.write(s)
    print("finish")

if __name__ == "__main__":
    main()