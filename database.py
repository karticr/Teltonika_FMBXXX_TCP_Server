import pymongo
import os
import json

from avlMatcher import avlIdMatcher 

avl = avlIdMatcher()

class mongoController:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://192.168.1.160:27017/", username='skyalert', password='1198jbakhf')
        self.db     = self.client['teltonika']
        self.reg    = self.db['trackers']
        self.trackers_info = self.loadTrackerInfo()

    def isRegisterd(self, imei):
        return bool(self.reg.find_one({"imei":imei}))
    
    def RegisterTracker(self, data):
        if(not self.isRegisterd(data['imei'])):
            return bool(self.reg.insert_one(data))

    def getTrackerOutputs(self, imei):
        if(self.isRegisterd(imei)):
            data   = self.reg.find_one({'imei': imei})
            n1s    = data['io_data']['n1']
            t_info = self.trackers_info[imei]
            o_info = t_info['outputs']
            total  = o_info['total']
            ids    = o_info['ids']
            o_data = ""
            for i in ids:
               o_data = o_data + str(n1s[i])
        return o_data

    def updateRecState(self, boat_id, state):
        return bool(self.reg.find_one_and_update({"boat-id":boat_id},
                                            {"$set":{"rec-state": state}}))

    def updateBoat(self, data):
        return bool(self.reg.find_one_and_update({"boat-id":data["boat-id"]},
                                                {"$set":data}))
    def findTracker(self, id):
        return self.reg.find_one({'imei': id})
    


    def loadTrackerInfo(self):
        with open('trackerIds.json') as f:
            data = json.load(f)
        return data

if __name__ == '__main__':
    a = mongoController()
    data = {
        'sys_time': '06/01/2021 04:43:54', 
        'codecid': 8, 
        'no_record_i': 1, 
        'no_record_e': 1, 
        'crc-16': 53322, 
        'd_time_unix': 1609888433000, 
        'd_time_local': '2021-01-06 04:43:53', 
        'priority': 0, 'lon': 801066466, 
        'lat': 130463916, 
        'alt': 0, 
        'angle': 0, 
        'satellites': 0, 
        'speed': 0, 
        'io_data': {
            'n1': {
                str(21): 3, 
                str(1): 0, 
                str(179): 0, 
                str(2): 0, 
                str(180): 0}, 
            'n2': {
                str(66): 11791, 
                str(205): 11492, 
                str(67): 4110
                }, 
            'n4': {
                str(72): 273
                }
            },
        'imei': '358480080551601'
    }

    # a.RegisterTracker(data)
    from_db = a.findTracker('358480080551601')
    io = from_db['io_data']
    # print(io)
    io_data = avl.idToAvl(io)
    # print(io_data)
    outputs = a.getTrackerOutputs('358480080551601')
    print(outputs)