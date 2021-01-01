data = b'00000000000001bc080900000176bc2c30f1002fbf481707c6c03a002900991100000009080100020103000400b300b4003200330001480118000000000176bc2b4691002fbf481707c6c03a002900991000000009080100020103000400b300b4003200330001480118000000000176bc2a5c35002fbf481707c6c03a002900991000000009080100020103000400b300b4003200330001480119000000000176bc2971d5002fbf481707c6c03a002900990f00000009080100020103000400b300b4003200330001480119000000000176bc288775002fbf481707c6c03a002900990e00000009080100020103000400b300b4003200330001480119000000000176bc279d15002fbf481707c6c03a002900991100000009080100020103000400b300b4003200330001480119000000000176bc26b2b5002fbf481707c6c03a002900990f00000009080100020103000400b300b4003200330001480119000000000176bc25c859002fbf481707c6c03a002900990f00000009080100020103000400b300b4003200330001480119000000000176bc24ddf9002fbf481707c6c03a002900991000000009080100020103000400b300b40032003300014801190000090000cb7f'
data = b'00000000000001bc080900000176bce01da0002fbf481707c6c03a001000990f00000009080100020103000400b301b401320033000148011d000000000176b9648c92002fbf4ac207c6bbed002000000400000009080100020103000400b300b40032003300014807d0000000000176b963a232002fbf4ac207c6bbed001d00000400000009080100020103000400b300b40032003300014807d0000000000176b962b7d5002fbf4ac207c6bbed001b00000400000009080100020103000400b300b40032003300014807d0000000000176b961cd75002fbf4ac207c6bbed001f00000500000009080100020103000400b300b40032003300014807d0000000000176b960e315002fbf4ac207c6bbed001e00000500000009080100020103000400b300b40032003300014807d0000000000176b95ff8b5002fbf4ac207c6bbed000000000000000009080100020103000400b300b40032003300014807d0000000000176b95f0e55002fbf4ac207c6bbed001900000400000009080100020103000400b300b40032003300014807d0000000000176b95e23f9002fbf4ac207c6bbed000000000000000009080100020103000400b300b40032003300014807d000000900002d87'
data = b'000000000000003608010000016B40D8EA30010000000000000000000000000000000105021503010101425E0F01F10000601A014E0000000000000000010000C7CF'
import binascii
from binascii import unhexlify
import datetime
import json


from avlMatcher import avlController

avl = avlController()

def unixtolocal(unix_time):
    time = datetime.datetime.fromtimestamp(unix_time/1000)
    return f"{time:%Y-%m-%d %H:%M:%S}"

def avlDecode(data, total):
    # print(data)
    data = data.decode()
    single_size = int(len(data)/total)
    latest_data = data[0:single_size]
    print(latest_data)
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

    print("event io")

    print(eventIO_ID)
    print(N_Tot_id)
    print(n_N1)

    print("-------------")
    N1s_size   = n_N1*2*2
    N1s        = data[54:54+N1s_size]
    print(N1s)
    # print("id", N1s[0:0+2])

    dataall    = data[48:]
    print(dataall)



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

    print(fin)


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
    codecid     = int(data[16:18], 16)
    no_record_i = int(data[18:20], 16)      #first no of total records
    no_record_e = int(data[-10:-8], 16)     #no of total records before crc-16 check
    crc_16      = int(data[-8:],16)            #crc-16 check

    print('tot records', no_record_i, no_record_e, "crc:", crc_16)

    entries =  data[20:-10]
    # print(entries)
    print("------------")
    d_size   = len(entries)
    division = int(len(entries)/ no_record_i)

    e_list = []
    for i in range(0, d_size, division):
        e_list.append(entries[i:i+division])

    print(e_list[0])
    e_1 = e_list[0]                                 #AVL Complete packet

    # for i in e_list:
    #     print("dd", i)

    timerrr = e_1[0:16]
    tie     = int(timerrr, 16)
    local   = unixtolocal(tie)

    print("timer", timerrr)
    print("unix", tie)
    print("local", local)

    print("-------------")
    print("avl io", e_1[48:])                                # AVL IO packet 


    # print('len', int(data[20:], 16))
    # avlDecode(data[20:-10], record)
    # print("records", record)
    # print(int(data[-10:-8], 16))
    # return vars

print(decodeVars(data))









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