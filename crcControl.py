import libscrc

from toBytes import hexToBytes

class crcControl():
    def crcGen(self, msg, byte_size=4, endian='big'):
        encoded_msg = bytes.fromhex(msg)            #encode message to bytes for crc
        crc16_raw   = libscrc.ibm(encoded_msg)      # generate crc using CRC-16-IBM Reversed
        crc_in_bytes= hexToBytes(crc16_raw, 4)      # converting crc into 4 bytes
        crc_in_hex  = crc_in_bytes.hex()            # converting crc into hex
        return {"hex": crc_in_hex, "bytes": crc_in_bytes}



if __name__ == '__main__':
    a = crcControl()
    msgs = "0C01050000000e7365746469676f7574203120363001"
    a.crcGen(msgs)