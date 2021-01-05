import libscrc

class crcControl():
    def __inint__(self):
        self.b = "yolo"

    def crcGen(self, msg, byte_size=4, endian='big'):
        encoded_msg = bytes.fromhex(msg)
        crc16_raw   = libscrc.ibm(encoded_msg)
        crc_in_bytes= crc16_raw.to_bytes(byte_size, byteorder=endian)
        crc_in_hex  = crc_in_bytes.hex()
        # print(crc_in_bytes)
        # print(crc_in_hex)
        return {"hex": crc_in_hex, "bytes": crc_in_bytes}



if __name__ == '__main__':
    a = crcControl()
    msgs = "0C01050000000e7365746469676f7574203120363001"
    a.crcGen(msgs)