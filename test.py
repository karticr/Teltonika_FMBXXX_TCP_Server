data = b'00000000000001bc080900000176c1d407e2022fbf452907c6befd001f00001000000209080100020103000400b300b400320033000148011d000000000176c1d3fca4022fbf452907c6befd001f00001000000209080100020003000400b300b400320033000148011d000000000176c152faca022fbf491107c6c260002c00170900000209080100020103000400b300b4003200330001480119000000000176c152f04f022fbf491107c6c260002c00170800000209080100020003000400b300b4003200330001480119000000000176c152ec40022fbf491107c6c260002c00170800000209080100020103000400b300b4003200330001480119000000000176c152dfc1022fbf491107c6c260002c00170800000209080100020003000400b300b4003200330001480119000000000176c152a6b7022fbf491107c6c260002c00170800000209080100020103000400b300b4003200330001480119000000000176c1528869022fbf491107c6c260002c00170800000209080100020003000400b300b4003200330001480119000000000176c1528253022fbf491107c6c260002c00170800000209080100020103000400b300b40032003300014801190000090000a013'
import binascii
from binascii import unhexlify
import datetime
import json


from avlMatcher import avlIdMatcher

avl = avlIdMatcher()

def unixtolocal(unix_time):
    time = datetime.datetime.fromtimestamp(unix_time/1000)
    return f"{time:%Y-%m-%d %H:%M:%S}"

def avlDecode(data, total):
    # print(data)
    data = data.decode()
    single_size = int(len(data)/total)
    latest_data = data[0:single_size]
    # print(latest_data)
    time       = int(data[0:16], 16)
    priority   = int(data[16:18], 16)
    lon        = int(data[18:26], 16)
    lat        = int(data[26:34], 16)
    alt        = int(data[34:38], 16)
    angle      = int(data[38:42], 16)
    satellites = int(data[42:44], 16)
    speed      = int(data[44:48], 16)
    eventIO_ID = int(data[48:50], 16)
    N_Tot_id   = int(data[50:52], 16)
    n_N1       = int(data[52:54], 16)

    # print("event io")

    # print(eventIO_ID)
    # print(N_Tot_id)
    # print(n_N1)

    # print("-------------")
    N1s_size   = n_N1*2*2
    N1s        = data[54:54+N1s_size]
    # print(N1s)
    # print("id", N1s[0:0+2])

    dataall    = data[48:]
    # print(dataall)



    fin = {
        "time": time,
        "priority":priority,
        "gps":{"lat":lat, "lon":lon},
        "alt":alt,
        "angle": angle,
        "sats": satellites,
        "speed":speed,
        "eventIO ID":eventIO_ID,
        "N_Tot_id":N_Tot_id,
        "N1": n_N1
    }

    # print(fin)


    # print('single', len(data)/total)
    # new = []
    # new = data.split("0000017")
    # d = "0000017"
    # new = [d+e for e in data.split(d) if e]
    # # print(new)
    # for i in new:
    #     # print(len(i))
    #     # print(i)
    #     unix_time = int(i[:16], 16)
    #     print(unix_time)
    #     time = unixtolocal(unix_time)
        # print(time)



    # print(int(data[0:16], 16))


def decodeVars(data):
    data_field_length = int(data[8:16], 16)     # Data Field Length – size is calculated starting from Codec ID to Number of Data 2.
    codecid     = int(data[16:18], 16)
    no_record_i = int(data[18:20], 16)      #first no of total records
    no_record_e = int(data[-10:-8], 16)     #no of total records before crc-16 check
    crc_16      = int(data[-8:],16)            #crc-16 check
    
    print('tot records', no_record_i,"end:", no_record_e, "crc:", crc_16)

    data_field_length = data_field_length * 2
    # print("field length: ", data_field_length)

    end = data[16+data_field_length-2:]

    # print(len(end))
    # print("raw", end[0:2])
    # print("end:", int(end[0:2], 16))
    # print("crc:", int(end[2:], 16))

    

    entries =  data[20:-10]
    # print(entries)
    # print("------------")
    d_size   = len(entries)
    division = int(len(entries)/ no_record_i)

    e_list = []
    for i in range(0, d_size, division):
        e_list.append(entries[i:i+division])

    print("latest:", e_list[0])
    e_1 = e_list[0]                                 #AVL Complete packet

    # for i in e_list:
    #     print("dd", i)

    timerrr = e_1[0:16]
    tie     = int(timerrr, 16)
    local   = unixtolocal(tie)

    # print("timer", timerrr)
    # print("unix", tie)
    # print("local", local)

    # print("-------------")
    # print("avl io", e_1[48:])                                # AVL IO packet 


    # print('len', int(data[20:], 16))
    avlDecode(data[20:-10], no_record_i)
    print("no records", no_record_i)
    # print(int(data[-10:-8], 16))
    return vars

decodeVars(data)









def encoder(command):
    base_hex = "".join("{:02x}".format(ord(c)) for c in command)
    print(len(base_hex))
    beg = 0
    beg = beg.to_bytes(4, byteorder = 'big')

    print(beg)
    print(id(binascii.a2b_hex(base_hex)).to_bytes(28, byteorder = 'big'))
    return base_hex






# print(decodeVars(data))


# td = "00 00 00 00 00 00 00 16 0C 01 05 00 00 00 0E 73 65 74 64 69 67 6f 75 74 20 31 20 36 30 01 00 00 B3 3E"
# td = td.replace(" ", "")

# print(binascii.a2b_hex(td))
# print(unhexlify(td))
# print(bytes.fromhex(td))
# print(td.decode('hex'))



# a = "setdigout 1 60"
# print(encoder(a))