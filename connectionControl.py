import traceback
import json
from time import sleep
from threading import Thread

from database import mongoController
from msgEncoder import msgEncoder
from apiControl import postRequest

db = mongoController()
msg_encoder    = msgEncoder()
post_requester = postRequest()

class connControl:
    def __init__(self):
        self.active_connections = {}
        self.trackers_info = self.loadTrackerInfo()
        th = Thread(target=self.postRequester)
        th.start()

    def addNew(self, connection):
        imei = connection['imei']
        conn = connection['conn']
        print("added new connection to post control")
        self.active_connections[imei] = conn

    def removeConnection(self,imei):
        try:
            print("connection deleted")
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
            for imei in self.active_connections:
                # print("ime",imei)
                conn = self.active_connections[imei]
                # data = db.getTrackerOutputs(imei)
                data = db.findTracker(imei)
                app_server_resp = post_requester.postToServer(data)
                print("----------------------------------------------")
                if(app_server_resp != -1):
                    t_info = self.trackers_info.get(imei) or -1
                    if(t_info == -1):
                        return -1010
                    else:
                        total   = t_info['outputs']['total']
                        outputs = t_info['outputs']['ids']
                        db_output_data = {}
                        for i in range(total):
                            db_output_data[outputs[i]] = int(app_server_resp[i])
                        
                        print("db update data", db_output_data)
                        db.updateTrackerOutputs(imei, db_output_data)
                        msg ='setdigout ' + app_server_resp
                        print("to server", msg)
                        to_tracker = msg_encoder.msgToCodec12(msg, 'cmd')
                        conn.sendall(to_tracker)

                print("data to server",data)
                print("----------------------------------------------")
            sleep(5)

    def loadTrackerInfo(self):
        with open('trackerIds.json') as f:
            data = json.load(f)
        return data

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
