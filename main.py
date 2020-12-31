import socket
import threading
import binascii
import asyncio
from websocket import create_connection # websockets package
import time
import json
import datetime
import struct

accepted = False

class TCPServer():
    def __init__(self):
        self.port = 5001
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))

    def tcpServer(self):
        self.sock.listen()
        while True:
            print("here ?")
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    def handle_client(self,conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            print("waiting for device")
            data = conn.recv(1024)
            if(data):
                print(data)
                imei = binascii.hexlify(data)#.decode('utf-8')
                print(imei)
        print("how ?")
        conn.close()

    def decoder(self, raw):
        decoded = binascii.hexlify(raw)
        return decoded

    def getDateTime(self):
        return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def mResponse(self, data):
        record = int(data[18:20], 16)
        # resp = "0000" + str(record).zfill(4)
        print("no data", record)
        return record



if __name__ == '__main__':
    data = TCPServer()
    data.tcpServer()