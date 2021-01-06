import requests
from avlMatcher import avlIdMatcher
import json

avl_match = avlIdMatcher()
class postRequest():
    def __init__(self):
        self.post_url = "https://api.skymarinealert.co.uk/boats/endpoint"

    def postToServer(self, raw_data):
        io = avl_match.idToAvl(raw_data['io_data'])
        print("io", io)
        formatted_data = self.avlToPostData(raw_data, io)
        # print("after format",formatted_data)
        server_resp    = self.post(formatted_data)
        control = server_resp.text
        control = json.loads(control)

        control = control['response']
        resp = control.get('outputs') or -1
        if( resp != -1):
            print("okay?")
            data = self.serverToTracker(control['outputs'])
            # print('digoutdata', data)
            return data
        
        return -1

    def post(self,data, url = None):
        url = url if url else self.post_url
        res = requests.post(url, json=data)
        # print("status", res.status_code)
        print("text", res.text)
        return res

    def avlToPostData(self, avl, io):
        format = {
            "deviceId": avl['imei'],
            "nmea": {
                "lat" : str(avl['lat']/10000000),
                "long": str(avl['lon']/10000000),
                "speed"   : int(avl['speed'])
            },
            "inputs":{
                "temp1"      : (io.get('Dallas Temperature 1') or  0)/10,
                "bat_volt"   : (io.get('External Voltage') or 0)/1000,
                "track_volt" : (io.get('Battery Voltage') or 0)/1000,
                "pir"        : io.get('Digital Input 2') or 0
            },
            "outputs":{
                "led"   :io.get('Digital Output 1') or 0,
                "buzzer":io.get('Digital Output 0') or 0
            },
            "signal":{
                "mSing": int(io.get('GSM Signal') or 0),
                "mOp"  : io.get('GSM Cell ID')
            }
        }
        return format

    def serverToTracker(self, data):
        temp=[]
        for i in data:
            if(i=='led'):
                temp.append(str(data[i]))
            else:
                temp.append('0')
            if(i=='buzzer'):
                temp.append(str(data[i]))
            else:
                temp.append('0')
        new = ''.join(temp)
        return new

if __name__ == "__main__":
    data = {    
                'imei': '352093081429150',
                'sys_time': '03/01/2021 02:31:12',
                'codecid': 8,
                'no_record_i': 8,
                'no_record_e': 8,
                'crc-16': 54268,
                'd_time_unix': 1609621190808,
                'd_time_local': '2021-01-03 02:29:50',
                'priority': 2,
                'lon': 801065150,
                'lat': 130466366,
                'alt': 21,
                'angle': 289,
                'satellites': 10,
                'speed': 0,
                'io_data': {
                    'n1': {
                        1: 0,
                        2: 1,
                        3: 0,
                        4: 0,
                        179: 0,
                        180: 1,
                        50: 0,
                        51: 0
                    },
                    'n2': {
                        72: 277
                    }
                }
            }

    # print(data)
    a       = postRequest()
    ready   = a.postToServer(data)
    print(ready)