import traceback

class IODecoder():
    def __init__(self):
        self.IO_data = ""
        self.Ns_data = {}

        # These are the two most-supported Teltonika data sending protocols, Codec 8 and Codec 8E (8E hex = 142 decimal)
        self.codec_options = {
            142: {'id_size':2,'variable_length':True},   # 142 is decimal of 8E https://wiki.teltonika-gps.com/view/Codec#Codec_8_Extended
            8:   {'id_size':1,'variable_length':False},  # Biggest difference between 8 and 8E is the length of the AVL IDs and the presence of variable-length values after the N8 Properties
        }     
        
    def ioVariableDecoderNX(self, NXs, n_NX): # No NX_size because the size of the value is determined by 2 bytes after each ID
        cursor = 0
        temp = {}
        for idval in range(0,n_NX):
            id              = int(NXs[cursor:cursor+4], 16)
            length          = int(NXs[cursor+4:cursor+8], 16)
            val             = int(NXs[cursor+8:length*2], 16)
            cursor          = cursor + length * 2 + 8
            temp[id]        = val
        return(temp)
    
    def ioStaticDecoder(self, NPs, NPs_size,property,codecid):
        temp = {}
        id_size_b           = self.codec_options[codecid]['id_size'] * 2
        value_size_b        = property * 2
        idval_size          = id_size_b + value_size_b
        for i in range(0, NPs_size, idval_size):
            try:
                id          = int(NPs[i:i+id_size_b], 16)
                val         = int(NPs[i+id_size_b:i+id_size_b+value_size_b], 16)
                temp[id]    = val
            except ValueError:
                pass
        return(temp)

    def dataDecoder(self, n_data,codecid): # n_data is the entire received data from 48 on. 0:48 constitutes the preamble, data field and codec (maybe also number of data 1?)
        Ns_data = {}
        properties          = [1,2,4,8]                 # These are the different byte sizes of IO values that can be present
        eventIO_ID          = int(n_data[0:4], 16)      # This is the IO ID that triggered the record (0 if scheduled)
        N_Tot_io            = int(n_data[4:8], 16)      # Total number of IOs in this AVL packet
        cursor              = 8                         # Cursor starts at 8 because 0:4 is the eventIO_ID and 4:8 is the total number of IO items
        counted_IOs         = 0

        for property in properties:
            n_NP            = int(n_data[cursor:cursor+4], 16)
            NPs_size        = n_NP * ((self.codec_options[codecid]['id_size'] + property) * 2)  # Add the size of the ID and the size of the value, then multiply by the number of ID+value pairs in that property group to get the entire size
            NPs             = n_data[4+cursor:4+cursor+NPs_size]
            NP_data         = self.ioStaticDecoder(NPs, NPs_size, property,codecid)
            n_name          = 'n'+str(property)
            Ns_data[n_name] = NP_data   
            counted_IOs     = counted_IOs + n_NP
            cursor          = cursor + NPs_size + 4     # I still don't fully understand why I add an extra 4 here. That would mean I'm skipping over 2 bytes, right?

        if self.codec_options[codecid]['variable_length'] == True:
            n_NX            = int(n_data[cursor:cursor+4], 16)
            NXs             = n_data[cursor+4:-10]
            Ns_data['nX']   = self.ioVariableDecoderNX(NXs, n_NX)
            counted_IOs     = counted_IOs + n_NX


#        print('Counted IOs == Expected?',N_Tot_io==counted_IOs,counted_IOs,N_Tot_io)
        merged_dict = {k: v for d in Ns_data.values() for k, v in d.items()} # A merged dicitonary of all AVL IDs and their values without the n1, n2, holding dictionaries
#        print('merged_dict',merged_dict)
#        return(Ns_data)
        return(merged_dict)

        '''
        try:
            Ns_data    = {}
            eventIO_ID = int(n_data[0:4], 16)
            N_Tot_io   = int(n_data[4:8], 16)
            n_N1       = int(n_data[8:12], 16)                  # number of n1's
            N1s_size   = n_N1 * (4 + 2)                         # n1 size
            N1s        = n_data[12:12+N1s_size]                   # n1 raw data
            N1_data    = self.ioDecoderN1(N1s, N1s_size)
            Ns_data['n1'] = N1_data                             # final N1 converted

#            print('n_N1',n_N1)
#            if(n_N1 == N_Tot_io):                               # N1 Break check
#                print("breaking @ N1")
#                return Ns_data

            N2_start   = N1s_size + 12                          # n2 start location
            # N1s_size is the size of the N1s, but it starts 12 after the beginning, so add 12
            n_N2       = int(n_data[N2_start:N2_start+4], 16)   # number of n2's
            N2s_size   = n_N2 * (4 + 4)                         # n2 size The 4 + 4 represents the width of the ID and width of the value, All IO IDs are 2 bytes (4 in pythonspeak). N2 values are 2 bytes (4 in pythonspeak)
            N2_end     = N2_start+N2s_size+4                   # n2 end location # need to add at least 4 to account for...something. Maybe for the last ID/value pair?
            N2s        = n_data[N2_start+4: N2_end]             # n2 raw data # correct!
            N2_data    = self.ioDecoderN2(N2s, N2s_size)
            Ns_data['n2'] = N2_data                             # final N2 converted
#            print('n_N2',n_N2)

#            if(n_N1 + n_N2 == N_Tot_io):                        # N2 Break check
#                print("breaking @ N2")
#                return Ns_data

            N4_start   = N2_end                                 # n4 start location
            n_N4       = int(n_data[N4_start:N4_start+4], 16)   # number of n4's
            N4s_size   = n_N4 * (4 + 8)                         # n4 size
            N4_end     = N4_start + N4s_size + 4                # n4 end location # Not sure about the +4...maybe +8 since this is N4 group? I'm not sure
            N4s        = n_data[N4_start+4: N4_end]             # n4 raw data
            N4_data    = self.ioDecoderN4(N4s, N4s_size)
            Ns_data['n4'] = N4_data   
#            print('n_N4',n_N4)                          # final N4 converted
#            print('N4_end',N4_end)

#            if(n_N1 + n_N2 + n_N4 == N_Tot_io):                 # N4 Break check
#                print("breaking @ N4")
#                return Ns_data
            
            N8_start  = N4_end                                  # n8 start location
            n_N8Bytes = n_data[N8_start:N8_start+4]
            n_N8      = int(n_data[N8_start:N8_start+4], 16)    # number of n8's
            N8s_size  = n_N8 * (4 + 16)                         # n8 size
            N8_end    = N8_start + N8s_size +4                 # N8 end location
            N8s       = n_data[N8_start+4: N8_end]              # n8 raw data
            N8_data   = self.ioDecoderN8(N8s, N8s_size)         
            Ns_data['n8'] = N8_data                             # final N4 converted
#            print('n_N8',n_N8)
#            print('total length of n_data',len(n_data))
#            print('nearby N8 start data',n_data[N8_start-4:N8_start+4])

            a = [0,N1s_size+12,N2_start,N2_end,N4_start,N4_end,N8_start,N8_end]
#            print('N8s',N8s)

            NX_start  = N8_end
            n_nXBytes = n_data[NX_start:NX_start+4]
            n_NX      = int(n_data[NX_start:NX_start+4], 16)
            NX_end    = -10                                     # beginning of the postamble
            NXs       = n_data[NX_start+4:NX_end]
            NX_data   = self.ioDecoderNX(NXs,n_NX)
            Ns_data['nX'] = NX_data
#            print('N8_end to postamble',n_data[N8_end:-10])
#            print('n_NX',n_NX)
            print('N_Tot_io',N_Tot_io)
            print('sum of ios',n_N1 + n_N2 + n_N4 + n_N8+ n_NX)

            # Mr. Evans. You just successfully decoded an entire record. Nice work.


            if(n_N1 + n_N2 + n_N4 + n_N8 + n_NX == N_Tot_io):          # N4 Break check
                # Because codec 8E allows for a record to be broken into multiple data transmission chunks
                # And because I don't know/have enough time to figure out how to stich them back together
                # The sum of the Ns probably won't equal the given total, so return the data you have in either case
#                print("breaking @ N8")
                return(Ns_data)
            else:
                return(Ns_data)
#                return -1                                       # -1 error
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            return(Ns_data)
    '''

        

    def getNSData(self):
        return self.Ns_data



if __name__ == '__main__':
#    n_data = "00000016000d00ef0000f00000150500c80300450300010000b30000020000030000b400007164010701017c0000070042302300431027000900ac0011fc150012008f0013fc33000600ac000200f10004bc8a00100004df1f00000000"   
    n_data = '0000001c000e00ef0000f00000150500c80000450100010000b30000020000030000b400007164010701017c0000fa00000b00b5000b00b60008004230200018000000431023000900ac0011fc0a0012009d0013fc32000600ac000f0000000300f10004bc8a00c70000000000100004df1f00000000'

    # n_data = "0103021503010101425E100000"
    # data = dataDecoder(n_data)
    # print(data)

    d = IODecoder()
#    print(d.dataDecoder(n_data))
    # print(d.getNSData())
    for i in range(0,10):
        try:
            print(i)
            print(d.dataDecoder(n_data[i:]))
        except Exception as e:
            print('failed',e)




