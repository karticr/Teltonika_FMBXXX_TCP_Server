import requests

class postRequest():
    def __init__(self):
        pass

    def post(self, url, data):
        res = requests.post(url, data=data)
        return res



if __name__ == "__main__":
    data = {
            "deviceId": "fmb_640_1",
            "nmea": {
                "lat": "13.0465650",
                "long": "80.1064433"
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
    a   = postRequest()
    url = "https://api.skymarinealert.co.uk/boats/endpoint"
    print(a.post(url, data))