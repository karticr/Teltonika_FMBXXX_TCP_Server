import requests
from avlMatcher import avlIdMatcher

avl_match = avlIdMatcher()
class postRequest():
    def __init__(self):
        pass

    def post(self, url, data):
        res = requests.post(url, data=data)
        return res

    def avlToPostData(self, avl):
        format = {
            "deviceId": avl['imei'],
            "nmea": {
                "lat": avl['lat']/10000000,
                "long": avl['lon']/10000000
            },
            "inputs":{
                "temp1": 20,
                "speed": 30,
                "angle": 40,
                "altitude": 50
            },
            "outputs":{
                "led":1,
                "buzzer":0
            }
        }
        return format

    def idToAvl(self, data):
        format = {}
        for i in data:
            n_data = data[i]
            for j in n_data:
                id      = str(j)
                id_name = avl_match.getAvlInfo(id)['name']
                value   = n_data[j]
                # print("Key: {}, Value: {}".format(id_name, value))
                format[id_name] = value            
        return format


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

    
    a       = postRequest()
    io_data = a.idToAvl(data['io_data'])
    print(io_data)
    print(io_data['Digital Input 2'])
    ready   = a.avlToPostData(data)


    # print(ready)
    # url = "https://api.skymarinealert.co.uk/boats/endpoint"
    # print(a.post(url, data))