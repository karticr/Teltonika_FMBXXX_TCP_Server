data = b'00000000000001bc080900000176bc2c30f1002fbf481707c6c03a002900991100000009080100020103000400b300b4003200330001480118000000000176bc2b4691002fbf481707c6c03a002900991000000009080100020103000400b300b4003200330001480118000000000176bc2a5c35002fbf481707c6c03a002900991000000009080100020103000400b300b4003200330001480119000000000176bc2971d5002fbf481707c6c03a002900990f00000009080100020103000400b300b4003200330001480119000000000176bc288775002fbf481707c6c03a002900990e00000009080100020103000400b300b4003200330001480119000000000176bc279d15002fbf481707c6c03a002900991100000009080100020103000400b300b4003200330001480119000000000176bc26b2b5002fbf481707c6c03a002900990f00000009080100020103000400b300b4003200330001480119000000000176bc25c859002fbf481707c6c03a002900990f00000009080100020103000400b300b4003200330001480119000000000176bc24ddf9002fbf481707c6c03a002900991000000009080100020103000400b300b40032003300014801190000090000cb7f'
import binascii
from binascii import unhexlify
import datetime



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

    N1s_size   = n_N1*2*2
    N1s        = data[54:54+N1s_size]
    print(N1s)
    # print("id", N1s[0:0+2])
    for i in range(0, N1s_size, 4):
        id  = int(N1s[i:i+2], 16)
        val = int(N1s[i+2:i+4], 16)

        print("id: {}, value: {}".format(id, val))
        print("----------------")

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
    codecid   = int(data[16:18], 16)
    record    = int(data[18:20], 16)
    timestamp = int(data[20:36], 16)
    lon       = int(data[38:46], 16)
    lat       = int(data[46:54], 16)
    alt       = int(data[54:58], 16)

    vars = {
        "codec" : codecid,
        "novars": record,
        "timestamp": timestamp,
        "gps":{"lon": lon, "lat": lat},
        "alt": alt
    }

    # print('len', int(data[20:], 16))
    avlDecode(data[20:-10], record)
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