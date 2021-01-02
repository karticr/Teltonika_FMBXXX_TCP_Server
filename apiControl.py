import requests

class postRequest():
    def __init__(self):
        pass

    def post(self, url, data):
        return



if __name__ == "__main__":
    data = {
            "deviceId": "fmb_640_1",
            "nmea": {
                "lat": "13.0465650",
                "long": "801064433"
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
    a = postRequest()