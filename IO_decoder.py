from avlMatcher import avlController
n_data = "0009080100020103000400b301b401320033000148011d000000000176b9648c92002fbf4ac207c6bbed002000000400000009080100020103000400b300b40032003300014807d0000000000176b963a232002fbf4ac207c6bbed001d00000400000009080100020103000400b300b40032003300014807d0000000000176b962b7d5002fbf4ac207c6bbed001b00000400000009080100020103000400b300b40032003300014807d0000000000176b961cd75002fbf4ac207c6bbed001f00000500000009080100020103000400b300b40032003300014807d0000000000176b960e315002fbf4ac207c6bbed001e00000500000009080100020103000400b300b40032003300014807d0000000000176b95ff8b5002fbf4ac207c6bbed000000000000000009080100020103000400b300b40032003300014807d0000000000176b95f0e55002fbf4ac207c6bbed001900000400000009080100020103000400b300b40032003300014807d0000000000176b95e23f9002fbf4ac207c6bbed000000000000000009080100020103000400b300b40032003300014807d00000"
n_data = "0009080100020103000400b301b401320033000148011d0000"
avl = avlController()

def ioDecoderN1(N1s, N1s_size):
    temp       = []
    for i in range(0,  N1s_size, 4):
        id  = int(N1s[i:i+2], 16)
        val = int(N1s[i+2:i+4], 16)
        temp.append({int(id):val})
    return temp
        # print("id: {}, value: {}".format(id, val))
        # print("id: {}, value: {}".format(avl.getAvlInfo(str(id))['name'], val))
        # print("----------------")

def ioDecoderN2(N2s, N2_size):
    print("n2s", N2s)
    temp = []
    for i in range(0, N2_size, 6):
        id  = int(N2s[i:i+2], 16)
        val = int(N2s[i+2: i+2+4], 16)
        temp.append({int(id):val})
    return temp


if __name__ == '__main__':

    eventIO_ID = int(n_data[0:2], 16)
    N_Tot_id   = int(n_data[2:4], 16)

    n_N1       = int(n_data[4:6], 16)       # number of n1's
    N1s_size   = n_N1 * (2 + 2)             # n1 size
    N1s        = n_data[6:6+N1s_size]       # n1 data

    print(N1s)

    print("eventId:{}, N total: {}, n_N1:{}".format(eventIO_ID, N_Tot_id, n_N1))
    N1_data    = ioDecoderN1(N1s, N1s_size)
    print("N1", N1_data)

    N2_start   = 6+N1s_size                             # n2 start location
    n_N2       = int(n_data[N2_start:N2_start+2], 16)   # number of n2's
    N2s_size   = n_N2 * (2 + 4)                         # n2 size
    N2_end     = N2_start+2+N2s_size                    # n2 end location
    N2s        = n_data[N2_start+2: N2_end]
    
    N2_data    = ioDecoderN2(N2s, N2s_size)
    print("N2", N2_data)

    N3_start   = N2_end