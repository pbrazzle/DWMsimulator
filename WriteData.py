''' This file write's data to DWM Memory depending on the write instrucion'''

TRd_size = 5


def writezero(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    writeport = int(row_number)
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)


    # Shifting the data within the TRd space to right and writing at the TRd head
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos):
        for j in range(writeport + TRd_size - 1, writeport, -1):
            memory[i][j] = memory[i][j-1]

    local_buff_start = nanowire_num_start_pos
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos):

        memory[i][writeport] = Local_row_buffer[local_buff_start]
        local_buff_start += 1

    # hex_num = ''
    # # Converting binary data at TRd head to Hex for verification/visualization
    # count = 0
    # s = ''
    #
    # # for j in range(writeport, writeport + TRd_size):
    # for i in range(0, 512):
    #     s += (str(memory[i][writeport]))
    #     count += 1
    #     if count == 4:
    #         num = int(s, 2)
    #         # print(hex(num))
    #         string_hex_num = format(num, 'x')
    #         hex_num += (string_hex_num)
    #         s = ''
    #         count = 0
    # print('W AP0 at TRd pos {} is {}'.format(writeport - 16, hex_num))

    hex_num = ''
    # Converting binary data at TRd head to Hex for verification/visualization
    count = 0
    s = ''
    for TRdlen in range( writeport, writeport + TRd_size):
        for i in range(0, 511 + 1):
            s += (str(memory[i][TRdlen]))
            count += 1
            if count == 4:
                num = int(s, 2)
                string_hex_num = format(num, 'x')
                hex_num += (string_hex_num)
                s = ''
                count = 0
        print("For 'W AP0 AP1' pos at {} data is {}".format(TRdlen - 16, hex_num))
        hex_num = ''

    return 1, 0.504676821

def writeone(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    writeport = int(row_number) + TRd_size - 1
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)


    # Shifting the data within the TRd space to left and writing at the TRd tail
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        for j in range(writeport - TRd_size + 1, writeport):
            memory[i][j] = memory[i][j+1]

    local_buff_start = nanowire_num_start_pos
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        memory[i][writeport] = Local_row_buffer[local_buff_start]
        local_buff_start += 1

    hex_num = []
    # Converting binary data at TRd head to Hex for verification/visualization
    count = 0
    s = ''
    for TRdlen in range(writeport - TRd_size + 1, writeport + 1):
        for i in range(0, 511 + 1):
            s += (str(memory[i][TRdlen]))
            count += 1
            if count == 4:
                num = int(s, 2)
                hex_num.append(hex(num))
                s = ''
                count = 0
        print('Data after memory transverse write AP1 at TRd pos {} is {}'.format(TRdlen, hex_num))
        hex_num.clear()

    return 1, 0.504676821

def overwrite_zero(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    writeport = int(row_number)
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)

    # Overwriting at the TRd head or tail
    local_buff_start = nanowire_num_start_pos
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        memory[i][writeport] = Local_row_buffer[local_buff_start]
        local_buff_start += 1

    # hex_num = []
    # # Converting binary data at TRd head to Hex for verification/visualization
    # count = 0
    # s = ''
    # for i in range(0, 512):
    #     s += (str(memory[i][writeport]))
    #     count += 1
    #     if count == 4:
    #         num = int(s, 2)
    #         hex_num.append(hex(num))
    #         s = ''
    #         count = 0
    # print('Data after memory overwrite at TRd head at writeport {} is {}'.format(writeport, hex_num))
    hex_num = ''
    # Converting binary data at TRd head to Hex for verification/visualization
    count = 0
    s = ''

    # for j in range(writeport, writeport + TRd_size):
    for i in range(0, 512):
        s += (str(memory[i][writeport]))
        count += 1
        if count == 4:
            num = int(s, 2)
            # print(hex(num))
            string_hex_num = format(num, 'x')
            hex_num+=(string_hex_num)
            s = ''
            count = 0
    print('W AP0 at TRd pos {} is {}'.format(writeport - 16 , hex_num))
    hex_num = ''

    return 1, 0.1

def overwrite_one(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    writeport = int(row_number)
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)

    # Overwriting at the TRd head or tail
    local_buff_start = nanowire_num_start_pos
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos+1):
        memory[i][writeport] = Local_row_buffer[local_buff_start]
        local_buff_start += 1

    # hex_num = []
    # # Converting binary data at TRd head to Hex for verification/visualization
    # count = 0
    # s = ''
    # for i in range(0, 511+1):
    #     s += (str(memory[i][writeport]))
    #     count += 1
    #     if count == 4:
    #         num = int(s, 2)
    #         hex_num.append(hex(num))
    #         s = ''
    #         count = 0
    # print('Data after memory overwrite at TRd tail at writeport {} is {}'.format(writeport, hex_num))
    hex_num = []
    # Converting binary data at TRd head to Hex for verification/visualization
    count = 0
    s = ''
    for TRdlen in range(writeport - TRd_size + 1, writeport + 1):
        for i in range(0, 512):
            s += (str(memory[i][TRdlen]))
            count += 1
            if count == 4:
                num = int(s, 2)
                hex_num.append(hex(num))
                s = ''
                count = 0
        print('Data after memory overwrite at TRd tail at TRd pos {} is {}'.format(TRdlen, hex_num))
        hex_num.clear()

    return 1, 0.1


# def shift_writezero(memory, data_in_binary):
#     # write at (right) TRd end and shift data towards right padding.
#     # data_in_binary = ''.join(format(ord(x), 'b') for x in data)
#
#     writeport = int(L/2)
#     memory[writeport] = data_in_binary
#
#     return 1
#
# def shift_writeone(memory, data_in_binary):
#     # write at (right) TRd end and shift data towards right padding.
#     # data_in_binary = ''.join(format(ord(x), 'b') for x in data)
#
#     writeport = int(L + L/2)
#     memory[writeport] = data_in_binary
#
#     print(memory)
#
#     return 1



def writezero_shiftLE(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    #write at (left) TRd start and shift data towards the left padding.
    writeport = int(row_number) + 16
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)

    # Shifting data left by 1 position towards left extremity
    start = 0
    for i in range(start, writeport):
        memory[i][nanowire_num_start_pos:nanowire_num_end_pos] = memory[i + 1][nanowire_num_start_pos:nanowire_num_end_pos]
    memory[writeport][nanowire_num_start_pos:nanowire_num_end_pos] = Local_row_buffer[nanowire_num_start_pos:nanowire_num_end_pos]

    return 1, 0.504676821


def writezero_shiftRE(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    #write at (left) TRd start and shift data towards the right padding.
    writeport = int(row_number) + 16
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)

    # Shifting data right by 1 position towards the right extremity.
    start = int(2*32)
    for i in range(start, writeport, -1):
        memory[i][nanowire_num_start_pos:nanowire_num_end_pos] = memory[i - 1][nanowire_num_start_pos:nanowire_num_end_pos]
    memory[writeport][nanowire_num_start_pos:nanowire_num_end_pos] = Local_row_buffer[nanowire_num_start_pos:nanowire_num_end_pos]

    return 1, 0.504676821

def writeone_shiftLE(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    #write at (right) TRd end and shift data towards left padding.
    writeport = int(row_number) + 16
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)

    # Shifting data left by 1 position
    start = 0
    for i in range(start, writeport):
        memory[i][nanowire_num_start_pos:nanowire_num_end_pos] = memory[i + 1][nanowire_num_start_pos:nanowire_num_end_pos]
    memory[writeport][nanowire_num_start_pos:nanowire_num_end_pos] = Local_row_buffer[nanowire_num_start_pos:nanowire_num_end_pos]

    return 1, 0.504676821

def writeone_shiftRE(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    #write at (right) TRd end and shift data towards right padding.
    writeport = int(row_number) + 16
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)

    # Shifting data left by 1 position
    start = int(2*32)
    for i in range(start, writeport, -1):
        memory[i][nanowire_num_start_pos:nanowire_num_end_pos] = memory[i - 1][nanowire_num_start_pos:nanowire_num_end_pos]
    memory[writeport][nanowire_num_start_pos:nanowire_num_end_pos] = Local_row_buffer[nanowire_num_start_pos:nanowire_num_end_pos]

    return 1, 0.504676821

