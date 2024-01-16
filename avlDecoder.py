import binascii,datetime,math,json
from IO_decoder import IODecoder
import libscrc
from crcControl import crcControl
crc = crcControl()


io  = IODecoder()
class avlDecoder():
    def __init__(self):
        self.raw_data = ""
        self.initVars()
       
    def initVars(self):            # initilizing variables
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

    def decodeAVL(self, data,avlids):
        self.raw_data      = data
        self.data_field_l  = int(data[8:16],16)*2                                  # Data Field Length – size is calculated starting from Codec ID to Number of Data 2.
        self.total_io_size = self.data_field_l-4-2                                 #-4=> subtract codecid and no of data, -2=> no of data at the end.
        self.io_end        = 20+self.total_io_size                                 # 20=> start from timestamp
        self.codecid       = int(data[16:18], 16)                                  # codecid
        self.no_record_i   = int(data[18:20], 16)                                  # first no of total records
        self.no_record_e   = int(data[-10:-8], 16)                                 # no of total records before crc-16 check
        self.crc_16        = int(data[-8:],16)                                     # crc-16 check
        self.first_io_start= 20                                                    # first io starting pos
        self.first_io_end  = math.ceil(self.total_io_size/ self.no_record_e)       # end pos for first io entry
        
        if(self.codecid in [142, 8] ):# and (self.no_record_i == self.no_record_e)):   # See codec_options in IO_decoder for more info on 142 and 8
            record_entries = data[self.first_io_start: self.io_end ]               # entry data
            entries_size     = len(record_entries)                                 # total no of entries
            division_size    = int(len(record_entries)/ self.no_record_i)          # division size
            self.avl_entries = []

#            print("old size:", entries_size, "division:", division_size)
#            print("new size:", self.total_io_size, "division:", self.total_io_size/ self.no_record_e)

            for i in range(0, entries_size, division_size): 
                self.avl_entries.append(record_entries[i:i+division_size])         # splitting into chunks
            
            self.avl_latest   = record_entries[0:self.first_io_end]                # latest avl data packets
            
#            self.avl_latest_1   = self.avl_entries[0]   

#            print("________________________________________")
#            print("old:", self.avl_entries[0])
#            print("new:", self.avl_latest)
#            print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

            self.d_time_unix  = int(self.avl_latest[0:16],16)                      # device time unix
            self.d_time_local = self.unixtoLocal(self.d_time_unix)                 # device time local
            self.priority     = int(record_entries[16:18], 16)                     # device data priority
            self.lon          = (int(record_entries[18:26], 16)-(1<<32))/10000000  # longitude
            self.lat          = int(record_entries[26:34], 16)/10000000            # latitude
            self.alt          = int(record_entries[34:38], 16)                     # altitude
            self.angle        = int(record_entries[38:42], 16)                     # angle
            self.satellites   = int(record_entries[42:44], 16)                     # no of satellites
            self.speed        = int(record_entries[44:48], 16)                     # speed
            
            self.avl_io_raw   = self.avl_latest[48:]                               # avl io data raw
#            print("raw io",self.avl_io_raw)                                       
            self.decoded_io   = io.dataDecoder(self.avl_io_raw,self.codecid)       # decoded avl data
#            print('self.decoded_io',self.decoded_io)

            self.translated_io= {}
            for id,value in self.decoded_io.items():
                if str(id) in avlids.keys():
                    self.translated_io.update({avlids[str(id)]['name']:value})
                else:
                    self.translated_io.update({id:value})



            return(self.getAvlData())
        else:
            print('self.codecid',self.codecid)
            print('self.no_record_i',self.no_record_i)
            print('self.no_record_e',self.no_record_e)
            return(False)
 
    def getDateTime(self):                                                         # system time
        return(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    def unixtoLocal(self, unix_time):                                              # unix to local time
        time = datetime.datetime.fromtimestamp(unix_time/1000)
        return(f"{time:%Y-%m-%d %H:%M:%S}")

    
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
#            "io_data"     :self.decoded_io,  
            "io_data"     :self.translated_io    

        }
        return(data)

    def getRawData(self):
        return self.raw_data

if __name__ == "__main__":
    avl = avlDecoder()
    flespirecs = {
#        'Data received(13/01/2024 08:14:42 size: 1185B tcp)':b'00000000000004958E0A0000018D0346AD2000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230200043101E000900AC0011FC130012009C0013FC31000600AC000200F10004BC8A00100004DF1F000000000000018D0347225000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C0000070042303A0043101E000900AC0011FC0A001200970013FC24000600AC000200F10004BC8A00100004DF1F000000000000018D0347978000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230360043101E000900AC0011FC130012009A0013FC2C000600AC000200F10004BC8A00100004DF1F000000000000018D03480CB000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C0000070042303D0043101E000900AC0011FC090012009A0013FC2F000600AC000200F10004BC8A00100004DF1F000000000000018D034881E000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C0000070042303D0043101E000900AC0011FC06001200980013FC33000600AC000200F10004BC8A00100004DF1F000000000000018D0348F71000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230360043101E000900AC0011FC170012009C0013FC32000600AC000200F10004BC8A00100004DF1F000000000000018D03496C4000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230380043101E000900AC0011FC0A0012009D0013FC31000600AC000200F10004BC8A00100004DF1F000000000000018D0349E17000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230410043101E000900AC0011FC060012009C0013FC2E000600AC000200F10004BC8A00100004DF1F000000000000018D034A56A000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C0000070042303A0043101E000900AC0011FC19001200A00013FC26000600AC000200F10004BC8A00100004DF1F000000000000018D034ACBD000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230200043101E000900AC0011FC0D001200980013FC30000600AC000200F10004BC8A00100004DF1F000000000A0000B269',
#        'Data received(13/01/2024 08:14:45 size: 1185B tcp)':b'00000000000004958E0A0000018D034B410000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230200043101E000900AC0011FC13001200990013FC33000600AC000200F10004BC8A00100004DF1F000000000000018D034BB63000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C0000070042302B0043101E000900AC0011FC09001200990013FC33000600AC000200F10004BC8A00100004DF1F000000000000018D034C2B6000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C0000070042303D0043101E000900AC0011FC1A0012009E0013FC2A000600AC000200F10004BC8A00100004DF1F000000000000018D034CA09000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230450043101E000900AC0011FC150012009A0013FC2C000600AC000200F10004BC8A00100004DF1F000000000000018D034D15C000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230410043101E000900AC0011FC0A001200980013FC30000600AC000200F10004BC8A00100004DF1F000000000000018D034D8AF000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230380043101E000900AC0011FC090012009B0013FC32000600AC000200F10004BC8A00100004DF1F000000000000018D034E002000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230410043101E000900AC0011FC060012009C0013FC2F000600AC000200F10004BC8A00100004DF1F000000000000018D034E755000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230340043101E000900AC0011FC0A0012009D0013FC32000600AC000200F10004BC8A00100004DF1F000000000000018D034EEA8000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C0000070042303A0043101E000900AC0011FC0B001200950013FC24000600AC000200F10004BC8A00100004DF1F000000000000018D034F5FB000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230430043101E000900AC0011FC130012009A0013FC2E000600AC000200F10004BC8A00100004DF1F000000000A0000F6B9',
#        'Data received(13/01/2024 08:14:46 size: 1185B tcp)':b'00000000000004958E0A0000018D0358FCA000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230200043101E000900AC0011FC14001200A20013FC28000600AC000200F10004BC8A00100004DF1F000000000000018D035971D000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C0000070042303F0043101E000900AC0011FC0A0012009E0013FC32000600AC000200F10004BC8A00100004DF1F000000000000018D0359E70000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C0000070042302B0043101E000900AC0011FC06001200900013FC38000600AC000200F10004BC8A00100004DF1F000000000000018D035A5C3000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230410043101E000900AC0011FC06001200A00013FC33000600AC000200F10004BC8A00100004DF1F000000000000018D035AD16000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C0000070042303D0043101E000900AC0011FC0A0012009D0013FC30000600AC000200F10004BC8A00100004DF1F000000000000018D035B469000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230410043101E000900AC0011FC050012009D0013FC31000600AC000200F10004BC8A00100004DF1F000000000000018D035BBBC000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C0000070042303D0043101E000900AC0011FC090012009C0013FC2E000600AC000200F10004BC8A00100004DF1F000000000000018D035C30F000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230340043101E000900AC0011FC130012009A0013FC32000600AC000200F10004BC8A00100004DF1F000000000000018D035CA62000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230320043101E000900AC0011FC0B001200990013FC28000600AC000200F10004BC8A00100004DF1F000000000000018D035D1B5000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C0000070042303D0043101E000900AC0011FC10001200970013FC33000600AC000200F10004BC8A00100004DF1F000000000A00000E95',
#        'Data received(13/01/2024 08:14:47 size: 600B tcp)':b'000000000000024C8E050000018D0362246000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230340043101E000900AC0011FC0A0012009D0013FC31000600AC000200F10004BC8A00100004DF1F000000000000018D0362999000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230200043101E000900AC0011FC16001200960013FC34000600AC000200F10004BC8A00100004DF1F000000000000018D03630EC000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C0000070042303D0043101E000900AC0011FC0A0012009E0013FC32000600AC000200F10004BC8A00100004DF1F000000000000018D036383F000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230300043101E000900AC0011FC100012009B0013FC32000600AC000200F10004BC8A00100004DF1F000000000000018D0363BAA001C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C0000070042303A0043101E000900AC0011FC0A0012009F0013FC31000600AC000200F10004BC8A00100004DF1F000000000500009550',
#        'Data received(13/01/2024 08:15:47 size: 249B tcp)':b'00000000000000ED8E020000018D03642FD000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230410043101E000900AC0011FC0B001200A80013FC21000600AC000200F10004BC8A00100004DF1F000000000000018D0364A50000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230380043101E000900AC0011FC0E001200A10013FC24000600AC000200F10004BC8A00100004DF1F00000000020000CFCD',
#        'Data received(13/01/2024 18:52:15 size: 483B tcp)':b'00000000000001D78E040000018D05A9C2A000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230250043101E000900AC0011FC190012009B0013FC32000600AC000200F10004BC8A00100004DF1F000000000000018D05AA37D000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230300043101D000900AC0011FC050012008E0013FC32000600AC000200F10004BC8A00100004DF1F000000000000018D05AAAD0000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230270043101E000900AC0011FC06001200980013FC33000600AC000200F10004BC8A00100004DF1F000000000000018D05AB223000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230380043101D000900AC0011FBFF001200900013FC36000600AC000200F10004BC8A00100004DF1F00000000040000D21F',
        'red truck':b'00000000000001558e010000018d035ac99001c15da68317cd3596067700000f00000000003c001600ef0000f00000150400c80000450100010000b30000020000030000b400007164010701017c00005100005200005957006f0000980000a00300e80000eb0000fa00001300b5000d00b6000700422f79001800000043106a000900ae001100000012ffc70013ffeb000600ae000f03e80054000000550000005a0000006e000000700000007303840097000000a80000000d00f10004bc8a00c70000000000100015d7d800530000000000570c4c50c0006400003880006600000000006700000000006900129c8d006b00000644007b00000000008600000000013000000000000500650000000000000000008400800010300004050205000080818004003002060000000000000000020700000000000000000001011a001a55303432322d30302c55303235332d30302c42313046312d3134010000ec2d'

    }
    avlids = {}
    with open('avlIds.json','r') as infile:
        avlids.update(json.load(infile))

    for key,value in flespirecs.items():
        print('\n\n')
        res = avl.decodeAVL(value,avlids)
        print(key)
        print(json.dumps(res,indent=2))
#        print(res)

'''
    # this one has satellites and altitude and stuff
    data = b'00000000000000918e010000018cff2d063000c16b933a17b66827064c00000d00000000001c000e00ef0000f00000150500c80000450100010000b30000020000030000b400007164010701017c0000fa00000b00b5000a00b60007004230200018000000431023000900ac0011fc14001200a40013fc2c000600ac000f0000000300f10004bc8a00c70000000000100004df1f00000000010000e0ce'
    # from red truck. Still haven't figured out how to stich records together
    data = b'00000000000001558e010000018d035ac99001c15da68317cd3596067700000f00000000003c001600ef0000f00000150400c80000450100010000b30000020000030000b400007164010701017c00005100005200005957006f0000980000a00300e80000eb0000fa00001300b5000d00b6000700422f79001800000043106a000900ae001100000012ffc70013ffeb000600ae000f03e80054000000550000005a0000006e000000700000007303840097000000a80000000d00f10004bc8a00c70000000000100015d7d800530000000000570c4c50c0006400003880006600000000006700000000006900129c8d006b00000644007b00000000008600000000013000000000000500650000000000000000008400800010300004050205000080818004003002060000000000000000020700000000000000000001011a001a55303432322d30302c55303235332d30302c42313046312d3134010000ec2d'
    # data = b'000000000000004308020000016B40D57B480100000000000000000000000000000001010101000000000000016B40D5C198010000000000000000000000000000000101010101000000020000252C'
    avl = avlDecoder()
    res = avl.decodeAVL(data)
    print(json.dumps(res,indent=2))
    # avldata = avl.getAvlData()
    # print(avldata)
'''

