import traceback
from time import sleep
from threading import Thread

class connControl:
    def __init__(self):
        self.active_connections = {}
        th = Thread(target=self.postRequester)
        th.start()

    def addNew(self, connection):
        imei = connection['imei']
        conn = connection['conn']
        print("added new connection to post control")
        self.active_connections[imei] = conn

    def removeConnection(self,imei):
        try:
            self.active_connections.pop(imei)
            return True
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return False

    def sendCommand(self, connection, command):
        pass
    
    def getActiveConnections(self):
        return self.active_connections

    def postRequester(self):
        while True:
            print("here post requester")
            print(self.getActiveConnections())
            sleep(5)
class test:
    def yolo(self):
        return yolo



if __name__ == '__main__':
    a = connControl()
    b = test()
    data = {
        "imei":"1234567",
        "conn": b
    }

    a.addNew(data)
    print(a.getActiveConnections())
    data = {
        "imei":"12345632",
        "conn": b
    }

    a.addNew(data)

    print(a.getActiveConnections())

    a.removeConnection("12345632")
    print(a.getActiveConnections())
    pass
