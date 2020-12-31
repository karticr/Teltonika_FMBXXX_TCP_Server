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
    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))

    def tcpServer(self):
        self.sock.listen()
        while True:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    def Communicator(self, conn):
        print("handshaking")
        accept_con_mes = '\x01'
        conn.send(accept_con_mes.encode('utf-8'))
        print("handshake complete")
        while True:
            data = conn.recv(1024)
            if(data):
                recieved = self.decoder(data)
                print(recieved)
                vars = self.decodeVars(recieved)
                print(vars)
                conn.send(self.mResponse(vars['record']))
            else:
                break


    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            print("waiting for device")
            imei_data = conn.recv(1024)
            if(imei_data):
                imei = imei_data.decode('utf-8')
                print(imei)
                self.Communicator(conn)
            else:
                break
        print("how ?")
        conn.close()

    def decodeVars(self, data):
        codecid   = int(data[16:17], 16)
        record    = int(data[18:20], 16)
        timestamp = int(data[20:36], 16)
        lon       = int(data[38:46], 16)
        lat       = int(data[46:54], 16)
        alt       = int(data[54:58], 16)

        vars = {
            "codec" : codecid,
            "novars": record,
            "timestamp": timestamp,
            "gps":{"lon": lon, "lat": lat},
            "alt": alt
        }
        return vars


    def decoder(self, raw):
        decoded = binascii.hexlify(raw)
        return decoded

    def getDateTime(self):
        return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def mResponse(self, data):
        return data.to_bytes(4, byteorder = 'big')



if __name__ == '__main__':
    port = 5001
    data = TCPServer(port)
    data.tcpServer()