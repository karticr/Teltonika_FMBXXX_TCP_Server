import datetime

class avlDecoder():
    def __init__(self):
        self.data = []
    
    def unixtoLocal(self, unix_time):
        time = datetime.datetime.fromtimestamp(unix_time/1000)
        return f"{time:%Y-%m-%d %H:%M:%S}"