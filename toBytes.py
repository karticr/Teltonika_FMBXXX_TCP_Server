def hexToBytes(msg, byte_size, endian='big'):
    in_bytes = msg.to_bytes(byte_size, byteorder=endian)
    return in_bytes


