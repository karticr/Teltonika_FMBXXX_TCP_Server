import binascii,datetime,math,json,crcmod


def crc16(data : bytearray, offset , length):
    if data is None or offset < 0 or offset > len(data)- 1 and offset+length > len(data):
        return 0
    crc = 0xFFFF
    for i in range(0, length):
        crc ^= data[offset + i] << 8
        for j in range(0,8):
            if (crc & 0x8000) > 0:
                crc =(crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return crc & 0xFFFF


#data = b'00000000000000ED8E020000018D03642FD000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230410043101E000900AC0011FC0B001200A80013FC21000600AC000200F10004BC8A00100004DF1F000000000000018D0364A50000C16B933A17B668270000000000000000000016000D00EF0000F00000150500C80300450300010000B30000020000030000B400007164010701017C000007004230380043101E000900AC0011FC0E001200A10013FC24000600AC000200F10004BC8A00100004DF1F00000000020000CFCD'
raw = b'\x00\x00\x00\x00\x00\x00\x00\xed\x8e\x02\x00\x00\x01\x8d\x05\x1f\xf90\x00\xc1k\x93:\x17\xb6h\'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x00\r\x00\xef\x00\x00\xf0\x00\x00\x15\x05\x00\xc8\x03\x00E\x03\x00\x01\x00\x00\xb3\x00\x00\x02\x00\x00\x03\x00\x00\xb4\x00\x00qd\x01\x07\x01\x01|\x00\x00\x07\x00B0=\x00C\x10\x1e\x00\t\x00\xac\x00\x11\xfc\x15\x00\x12\x00\x9e\x00\x13\xfc?\x00\x06\x00\xac\x00\x02\x00\xf1\x00\x04\xbc\x8a\x00\x10\x00\x04\xdf\x1f\x00\x00\x00\x00\x00\x00\x01\x8d\x05 n`\x00\xc1k\x93:\x17\xb6h\'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x00\r\x00\xef\x00\x00\xf0\x00\x00\x15\x05\x00\xc8\x03\x00E\x03\x00\x01\x00\x00\xb3\x00\x00\x02\x00\x00\x03\x00\x00\xb4\x00\x00qd\x01\x07\x01\x01|\x00\x00\x07\x00B08\x00C\x10\x1e\x00\t\x00\xac\x00\x11\xfc\x14\x00\x12\x00\xa2\x00\x13\xfc*\x00\x06\x00\xac\x00\x02\x00\xf1\x00\x04\xbc\x8a\x00\x10\x00\x04\xdf\x1f\x00\x00\x00\x00\x02\x00\x00\xc4"'
#data = binascii.hexlify(raw)
data = raw.hex()
bytehex = bytes.fromhex(data)

runner = bytehex
crc_16 = int(data[-8:],16)  
print('crc should be this',crc_16)
crc16_ibm_func = crcmod.mkCrcFun(poly=0x18005, initCrc=0x0000, xorOut=0x0000, rev=False)
print('a',crc16_ibm_func(runner))
crca = binascii.crc_hqx(runner,0)
print('b',crca)
crc16 = crcmod.mkCrcFun(0x18005, rev=False, initCrc=0xFFFF, xorOut=0x0000)
z = hex(crc16("5a0001".decode(raw)))
print('c',z)


#crc = crcmod.predefined.mkPredefinedCrcFun('crc-16')(raw[18:-10])
#print(crc_16,crc, raw[18:-10])
#crc = crcmod.predefined.mkPredefinedCrcFun('crc-16')(data[18:-10])
#print(crc_16,crc, data[18:-10])
'''
for i in range(0,len(data)-shortest):
#        crc = binascii.crc_hqx(data[i:end],0)
#        crc = crc16(data[i:end],0,14)
        crc = crcmod.predefined.mkPredefinedCrcFun('crc-16')(data[i:end])
        print(crc_16,crc, data[i:end])
        if crc == crc_16:
            print('found ya boi')
            break
'''
#https://crccalc.com/
#It seems like my code is treating the data as if its ascii text. Figure out how to pipe it straight binary or something
