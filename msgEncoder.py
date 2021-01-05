
class msgEncoder():
    def __init__(self):
        self.raw_msg    = ''

    def msgToCodec12(self, msg, cmd_type):
        self.zero_bytes = '00000000'
        self.codec_id   = 'OC'
        self.cmd_quant  = '01'
        self.cmd_type   = '05' if cmd_type == 'cmd' else '06'
        self.cmd_size   = len(msg).to_bytes(4, byteorder='big').hex()
        self.data_size  = len("ss")
        self.printer()
    def printer(self):
        print(self.zero_bytes, self.codec_id, self.cmd_quant, self.cmd_type, self.cmd_size)



if __name__ == '__main__':
    a = msgEncoder()
    msg = 'getinfo'
    cmd_type = 'cmd'
    a.msgToCodec12(msg, cmd_type)
    