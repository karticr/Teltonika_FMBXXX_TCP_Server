import libscrc

class crcControl():

    def hexToBytes(self, msg, byte_size, endian='big'):
        in_bytes = msg.to_bytes(byte_size, byteorder=endian)
        return in_bytes

    def crcGen(self, msg, byte_size=4, endian='big'):
        if type(msg) != type(b''):
            print('converting to bytes')
            encoded_msg = bytes.fromhex(msg)            #encode message to bytes for crc
        else:
            encoded_msg = msg
#            encoded_msg = bytes.fromhex(msg)            #encode message to bytes for crc

        crc16_int   = libscrc.ibm(encoded_msg)      # generate crc using CRC-16-IBM Reversed
        crc_in_bytes= self.hexToBytes(crc16_int, byte_size)      # converting crc into 4 bytes
        crc_in_hex  = crc_in_bytes.hex()            # converting crc into hex
        return {"hex": crc_in_hex, "bytes": crc_in_bytes,'int':crc16_int}

