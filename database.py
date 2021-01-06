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
            t_info = self.trackers_info.get(imei) or -1

            if(t_info == -1):
                return -1010
            o_info = t_info['outputs']
            total  = o_info['total']
            ids    = o_info['ids']
            o_data = ""
            for i in ids:
               o_data = o_data + str(n1s[i])
        return o_data
    
    def findTracker(self, id):
        return self.reg.find_one({'imei': id})

    def updateTracker(self, data):
        return bool(self.reg.find_one_and_update({"imei":data["imei"]},
                                                {"$set":data}))
 
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
    # data = {
        # 'sys_time': '06/01/2021 05:42:22', 
        # 'codecid': 8, 
        # 'no_record_i': 2, 
        # 'no_record_e': 2, 
        # 'crc-16': 2867, 
        # 'd_time_unix': 1609611610300, 
        # 'd_time_local': '2021-01-02 23:50:10', 
        # 'priority': 0, 
        # 'lon': 801064250, 
        # 'lat': 130465916, 
        # 'alt': 85, 
        # 'angle': 0, 
        # 'satellites': 6, 
        # 'speed': 0, 
        # 'io_data': {
        #     'n1': {
        #         str(1): 0, 
        #         str(2): 1, 
        #         str(3): 0, 
        #         str(4): 0, 
        #         str(179): 0, 
        #         str(180): 1, 
        #         str(50): 0, 
        #         str(51): 0
        #         }, 
        #     'n2': {
        #         str(72): 281
        #         }
        #     },
        # 'imei':'352093081429150'
        # }
    d_imei = '358480080551601'
    if(a.isRegisterd(d_imei)):
        from_db = a.findTracker(d_imei)
        io = from_db['io_data']
        print(io)
        io_data = avl.idToAvl(io)
        print(io_data)
        outputs = a.getTrackerOutputs(d_imei)
        print(outputs)
    else:
        a.RegisterTracker(data)

