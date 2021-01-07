
class connControl:
    def __init__(self):
        self.active_connections = {}
    
    def addNew(self, connection):
        imei = connection['imei']
        conn = connection['conn']
        self.active_connections[imei] = conn

    def removeConnection(self,connection):
        pass

    def sendCommand(self, connection, command):
        pass
    
    def getActiveConnections(self):
        return self.active_connections


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
    pass
