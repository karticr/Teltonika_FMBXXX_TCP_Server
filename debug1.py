import binascii

a = "getinfo"
data = binascii.hexlify(a.encode('utf-8'))

orig = "676574696E666F"
print(data)
print(orig.encode('utf-8'))