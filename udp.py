import socket
from ast import literal_eval
localIP     = "192.168.1.254"
localPort   = 5001
bufferSize  = 1024

msgFromServer       = "1"
bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams
while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    message = message.hex()


    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    #messajes= Encoding.ASCII.GetString(message)
    
    print(clientMsg)
    print(clientIP)
    print(bytesAddressPair)
   

    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)