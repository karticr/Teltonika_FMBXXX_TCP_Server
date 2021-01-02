import binascii
import datetime

from IO_decoder import IODecoder
io  = IODecoder()
class avlDecoder():
    def __init__(self):
        self.raw_data = ""
        self.initVars()

    def initVars(self):            #initilizing variables
        self.codecid        = 0
        self.no_records_i   = 0
        self.no_records_e   = 0
        self.crc_16         = 0
        self.avl_entries    = []
        self.avl_latest     = ""
        self.d_time_unix    = 0 
        self.d_time_local   = ""
        self.avl_io_raw     = ""
        self.priority       = 0
        self.lon            = 0
        self.lat            = 0
        self.alt            = 0
        self.angle          = 0
        self.satellites     = 0
        self.speed          = 0
        self.decoded_io     = {}

    def decodeAVL(self, data):
        self.raw_data      = data
        self.codecid       = int(data[16:18], 16)      # codecid
        self.no_record_i   = int(data[18:20], 16)      # first no of total records
        self.no_record_e   = int(data[-10:-8], 16)     # no of total records before crc-16 check
        self.crc_16         = int(data[-8:],16)        # crc-16 check
        
        # print(self.getAvlData())

        if(self.codecid == 8 and (self.no_record_i == self.no_record_e)):
            record_entries   = data[20:-10]                                        # entry data
            entries_size     = len(record_entries)                                 # total no of entries
            division_size    = int(len(record_entries)/ self.no_record_i)          # division size
            self.avl_entries = []
            for i in range(0, entries_size, division_size): 
                self.avl_entries.append(record_entries[i:i+division_size])         # splitting into chunks

            self.avl_latest   = self.avl_entries[0]                                # latest avl data packets
            print(self.avl_latest)
            self.d_time_unix  = int(self.avl_latest[0:16],16)                      # device time unix
            self.d_time_local = self.unixtoLocal(self.d_time_unix)                 # device time local
            self.priority     = int(record_entries[16:18], 16)                     # device data priority
            self.lon          = int(record_entries[18:26], 16)                     # longitude
            self.lat          = int(record_entries[26:34], 16)                     # latitude
            self.alt          = int(record_entries[34:38], 16)                     # altitude
            self.angle        = int(record_entries[38:42], 16)                     # angle
            self.satellites   = int(record_entries[42:44], 16)                     # no of satellites
            self.speed        = int(record_entries[44:48], 16)                     # speed
        
            self.avl_io_raw   = self.avl_latest[48:]                               # avl io data raw
            self.decoded_io   = io.dataDecoder(self.avl_io_raw)                    # decoded avl data
            
            return self.getAvlData()
        else:
            return -1
 
    def getDateTime(self):                                                         # system time
        return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def unixtoLocal(self, unix_time):                                              # unix to local time
        time = datetime.datetime.fromtimestamp(unix_time/1000)
        return f"{time:%Y-%m-%d %H:%M:%S}"
        
    def getAvlData(self):
        data = {
            "sys_time"   : self.getDateTime(),
            "codecid"    : self.codecid,
            "no_record_i": self.no_record_i,
            "no_record_e": self.no_record_e,
            "crc-16"     : self.crc_16,
            # "avl_entries": self.avl_entries,
            # "avl_latest" : self.avl_latest,
            "d_time_unix" : self.d_time_unix,
            "d_time_local": self.d_time_local,
            "priority"    :self.priority,  
            "lon"         :self.lon,
            "lat"         :self.lat,
            "alt"         :self.alt,       
            "angle"       :self.angle,     
            "satellites"  :self.satellites,
            "speed"       :self.speed,
            "io_data"     :self.decoded_io    
        }
        return data

    def getRawData(self):
        return self.raw_data


if __name__ == "__main__":
    data = b'000000000000002808010000016B40D9AD80010000000000000000000000000000000103021503010101425E100000010000F22A'
    data = b'000000000000037d080a00000176c0abc0100000000000000000000000000000000000160bef00f00050041504c80045020100b30002000300b40009b50000b60000422de6180000cd2ce5ce023b430e384400d409000002f100009df810001fef190000000176c0acaa700000000000000000000000000000000000160bef00f00050041503c80045020100b30002000300b40009b50000b60000422de6180000cd2ce5ce023b430e3b4400d409000002f100009df810001fef190000000176c0ad94d00000000000000000000000000000000000160bef00f00050041503c80045020100b30002000300b40009b50000b60000422de6180000cd2ce5ce023b430e404400d409000002f100009df810001fef190000000176c0ae7f300000000000000000000000000000000000160bef00f00050041504c80045020100b30002000300b40009b50000b60000422de5180000cd2ce5ce023b430e404400d409000002f100009df810001fef190000000176c0af69900000000000000000000000000000000000160bef00f00050041503c80045020100b30002000300b40009b50000b60000422de6180000cd2ce5ce023b430e464400d409000002f100009df810001fef190000000176c0b136800000000000000000000000000000000000160bef00f00050041503c80045020100b30002000300b40009b50000b60000422dee180000cd2ce5ce023b430e434400d409000002f100009df810001fef190000000176c0b220e00000000000000000000000000000000000160bef00f00050041504c80045020100b30002000300b40009b50000b60000422deb180000cd2ce5ce023b430e4a4400d409000002f100009df810001fef190000000176c0b30b400000000000000000000000000000000000160bef00f00050041503c80045020100b30002000300b40009b50000b60000422dea180000cd2ce5ce023b430e504400d509000002f100009df810001fef190000000176c0b3f5a00000000000000000000000000000000000160bef00f00050041504c80045020100b30002000300b40009b50000b60000422dc9180000cd2ce5ce023b430e4f4400d409000002f100009df810001fef190000000176c0b5c6780000000000000000000000000000000000160bef00f00050041503c80045020100b30002000300b40009b50000b60000422de8180000cd2ce5ce023b430e554400d409000002f100009df810001fef19000a00005e10'
    data = b'00000000000001b9080700000176be86f8c9002fbf481707c6c03a002600990d00000009080100020103000400b301b4013200330001480123000000000176be860e6d002fbf481707c6c03a002600990e00000009080100020103000400b301b4013200330001480122000000000176b3409ce0002fbf509e07c6bc94000f007206000000100a010002010300040016044703f0001504c800ef0106432699440000b50016b60014422f04180000000000000176b33fb283002fbf509e07c6bc94000e007206000000100a010002010300040016044703f0001504c800ef0106432699440000b50016b60013422f17180000000000000176b33ec823002fbf4ab207c6bc52000a006506000000100a010002010300040016044703f0001503c800ef010643269c440000b50016b60013422eff180000000000000176b33dddc3002fbf446107c6bf0e001e000006000000100a010002010300040016044703f0001503c800ef0106432699440000b50015b60013422f07180000000000000176b33cf363002fbf446107c6bf0e0021000006000000100a010002010300040016044703f0001504c800ef010643269c440000b50015b60013422f111800000000070000e258'
    data = b'00000000000001bc080900000176c1d407e2022fbf452907c6befd001f00001000000209080100020103000400b300b400320033000148011d000000000176c1d3fca4022fbf452907c6befd001f00001000000209080100020003000400b300b400320033000148011d000000000176c152faca022fbf491107c6c260002c00170900000209080100020103000400b300b4003200330001480119000000000176c152f04f022fbf491107c6c260002c00170800000209080100020003000400b300b4003200330001480119000000000176c152ec40022fbf491107c6c260002c00170800000209080100020103000400b300b4003200330001480119000000000176c152dfc1022fbf491107c6c260002c00170800000209080100020003000400b300b4003200330001480119000000000176c152a6b7022fbf491107c6c260002c00170800000209080100020103000400b300b4003200330001480119000000000176c1528869022fbf491107c6c260002c00170800000209080100020003000400b300b4003200330001480119000000000176c1528253022fbf491107c6c260002c00170800000209080100020103000400b300b40032003300014801190000090000a013'
    avl = avlDecoder()
    res = avl.decodeAVL(data)
    print(res)
    # avldata = avl.getAvlData()
    # print(avldata)


