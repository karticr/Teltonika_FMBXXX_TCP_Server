
class connControl():
    def _init__():
        self.active_connections = {}
    
    def addNew(self, connection):
        self.active_connections[connection['imei']] = connection['conn']

    def removeConnection(self,connection):
        pass

    def sendCommand(self, connection, command):
        pass
    
    def getActiveConnections(self):
        return self.active_connections


if __name__ == '__main__':
    pass
