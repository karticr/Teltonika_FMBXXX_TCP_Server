import socket
import threading
import binascii
import asyncio
import time
import json
import datetime
import struct
import traceback

from avlDecoder import avlDecoder
from apiControl import postRequest
from dbConnection import writerecord

avl_decoder    = avlDecoder()
post_requester = postRequest()
class TCPServer():
    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.bind(('', self.port))
        self.avlids = {}
        with open('avlIds.json','r') as infile:
            self.avlids.update(json.load(infile))
        
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
#                    print('data',data)
                    vars         = {}
                    recieved = self.decoder(data) # this just binascii hexlifyies the data
                    print('\nreceived',recieved)
                    with open('raw.txt', 'a+') as w:
                        w.writelines(recieved.decode('utf-8')+'\n')
                    vars = avl_decoder.decodeAVL(recieved,self.avlids)
                    vars['imei'] = imei.split("\x0f")[1]
                    print("vars", json.dumps(vars,indent=2))
#                    print('vars[io_data]',vars['io_data'])
                    resp = self.mResponse(vars['no_record_i'])
                    writerecord(vars)
                    print('resp',resp)
                    time.sleep(20)
                    conn.send(resp)
                    # conn.send(struct.pack("!L", vars['novars']))
                else:
                    break
            except Exception as e:
                print(traceback.format_exc())
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