import binascii
import libscrc
from crcControl import crcControl

crc = crcControl()

class msgEncoder():
    def __init__(self):
        self.raw_msg    = ''

    def msgToCodec12(self, msg, cmd_type):
        self.zero_bytes = '00000000'

        self.codec_id    = '0C'
        self.cmd_quant_1 = '01'
        self.cmd_type    = '05' if cmd_type == 'cmd' else '06'
        self.cmd_size    = len(msg).to_bytes(4, byteorder='big').hex()
        self.cmd         = binascii.hexlify(msg.encode('utf-8')).decode()
        self.cmd_quant_2 = '01'
        
        self.data_size  = int((len(self.codec_id) + len(self.cmd_quant_1) + len(self.cmd_type) + len(self.cmd_size) + len(self.cmd) + len(self.cmd_quant_2))/2).to_bytes(4, byteorder='big').hex()

        crc_data        = self.codec_id + self.cmd_quant_1 + self.cmd_type + self.cmd_size + self.cmd + self.cmd_quant_2
        # print("crc data",crc_data)
        self.crc        = crc.crcGen(crc_data)['hex']
        
        self.hex_msg    = self.zero_bytes+self.data_size+self.codec_id+self.cmd_quant_1+self.cmd_type+self.cmd_size+self.cmd+self.cmd_quant_2+self.crc
        
        self.printer()

    def printer(self):
        print(self.zero_bytes, self.data_size, self.codec_id, self.cmd_quant_1, self.cmd_type, self.cmd_size, self.cmd, self.cmd_quant_2, self.crc)



if __name__ == '__main__':
    a = msgEncoder()
    msg = 'setdigout 1 60'
    cmd_type = 'cmd'
    a.msgToCodec12(msg, cmd_type)
    