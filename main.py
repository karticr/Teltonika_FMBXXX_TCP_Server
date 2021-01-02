import socket
import threading
import binascii
import asyncio
import time
import json
import datetime
import struct

from avlDecoder import avlDecoder
from apiControl import postRequest

avl_decoder    = avlDecoder()
post_requester = postRequest()
class TCPServer():
    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.bind(('', self.port))

    def tcpServer(self):
        self.sock.listen()
        while True:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    def Communicator(self, conn, imei):
        accept_con_mes = '\x01'
        conn.send(accept_con_mes.encode('utf-8'))
        print("handshake complete")
        while True:
            try:
                data = conn.recv(1024)
                if(data):
                    vars         = {}
                    vars['imei'] = imei
                    recieved = self.decoder(data)
                    with open('raw.txt', 'a+') as w:
                        w.writelines(recieved.decode('utf-8')+'\n')
                    vars = avl_decoder.decodeAVL(recieved)
                    print("vars", vars)
                    resp = self.mResponse(vars['no_record_i'])
                    time.sleep(60)
                    conn.send(resp)
                    # conn.send(struct.pack("!L", vars['novars']))
                    print("done")
                else:
                    break
            except Exception as e:
                print(e)
                break
        print('exiting tcp comms')


    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            print("waiting for device")
            try:
                imei_data = conn.recv(1024)
                if(imei_data):
                    imei = imei_data.decode('utf-8')
                    print(imei)
                    self.Communicator(conn, imei)
                else:
                    break
            except Exception as e:
                # print(e)
                print("connection closed")
                conn.close()
                break
    
    def decodeVars(self, data, imei):
        curr_time = self.getDateTime()
        codecid   = int(data[16:18], 16)
        record    = int(data[18:20], 16)
        timestamp = int(data[20:36], 16)
        lon       = int(data[38:46], 16)
        lat       = int(data[46:54], 16)
        alt       = int(data[54:58], 16)

        vars = {
            "sys-time": curr_time,
            "imei"  : imei,
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