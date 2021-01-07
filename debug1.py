# import binascii
# import libscrc
# import crc16
# import sys
# # a = "getinfo"
# data = binascii.hexlify(a.encode('utf-8'))

# orig = "676574696E666F"
# print(data)
# print(orig.encode('utf-8'))


# test = "0000000F"
# print(int(test,16))

# data = '0x5D08'
# print(data)

# print(int(data, 16))

# crc_data    = "0C010500000007676574696e666f01"
# crc_encoded = bytes.fromhex(crc_data)
# crc16 = libscrc.ibm(crc_encoded)
# print(crc16)
# print(crc16.to_bytes(4, byteorder='big').hex())


# data = int("676574696e666f", 16)
# print(data)
# aa = data.to_bytes(7, byteorder='big')
# print(aa)
# sys.stdout.buffer.write(aa)


a = 2
b='00'
for i in range(a):
    print(i)
    print(b[i])