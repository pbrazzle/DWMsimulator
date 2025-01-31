'''
This is the script that uses the DWM simulator to run differrent algorithm.
'''
import config
import SubByte as SB
from main_controller import DBC

from math import floor
import argparse

# Calculate Cycle and Energy
total_energy = 0
total_cycles = 0

def get_address(address):
    '''Returns the DBC and row position for a given address'''
    DBC_number = floor(address / 32)
    row_number = address % 32
    return DBC_number, row_number

def call_DBC(dbc, row_number, operation, nanowire_start_pos, nanowire_end_pos, d=None):
    #Is operation a string or int?
    if operation == 'overwrite':
        param = dbc.controller(row_number, operation, nanowire_start_pos, nanowire_end_pos, d)
        return param
    elif operation == 1 or operation == 2 or operation == 3 or operation == 4 or operation == 5 or operation == 6:
        param = dbc.controller(row_number, operation, nanowire_start_pos, nanowire_end_pos, d)
        return param
    # elif operation == 'MULT':
    #     param, r = dbc.controller(row_number, operation, nanowire_start_pos, nanowire_end_pos)
    #     return param, r
    else:
        # Calling DBC object for each instruction above
        param, data = dbc.controller(row_number, operation, nanowire_start_pos, nanowire_end_pos)
        return param, data

def write_type(dbcs, row_number_destination, write_type, nanowire_num_start_pos, nanowire_num_end_pos, data_hex):
    # print('write_type',write_type, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
    write_type = int(write_type)
    if write_type == 0:
        # Type 0: Write back normally
        # Call Write
        param = call_DBC(dbcs, row_number_destination, 'overwrite',  nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
    elif write_type >= 1 and  write_type <= 6:
        # Type 1: Transverse writes
        param = call_DBC(dbcs, row_number_destination, write_type, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)

    elif write_type == 7:
        raise Exception("Sorry, no operation for seven")
    return  param

parser = argparse.ArgumentParser(
                description='SPIMulator: DWM Simulator')

parser.add_argument('instruction_file')
parser.add_argument('-l', '--length', type=int, default=512, help='Length of the nanowire. Default is 512')

args = parser.parse_args()

config.read_args(args)

# Parameter Table
perform_param = dict()
keys = ['write','TR_writes', 'read', 'TR_reads', 'shift', 'STORE']
perform_param = {key: 0 for key in keys}

# Creating 16 DBC objects
dbcs = [DBC() for i in range(16)]

#Reading Instruction of text file
instruction_file = open(args.instruction_file, 'r')

# Read single line in file
lines = instruction_file.readlines()

# Extracting each instruction from Lines:
break_out_flag = False
for line in lines:
    if line.strip():
        instruction_line = []
        for word in line.split():
            if not '//' in word:
                instruction_line.append(word)

        if instruction_line[0] == '#':
            continue
        print('instruction:', instruction_line)
        address_destination = instruction_line[1]
        address_destination = (address_destination.split("$", 1))
        address_destination = int(address_destination[1])
        DBC_number_destinantion, row_number_destination = get_address(address_destination)
        print('Destinantion DBC No:', DBC_number_destinantion)
        print('Destinantion Row No:', row_number_destination)


        nanowire_num_start_pos = 0
        nanowire_num_end_pos = config.get_nanowire_size() - 1

        if '$' in instruction_line[2]:
            address_source = instruction_line[2]
            address_source = (address_source.split("$", 1))
            address_source = (address_source[1])
            address_source = int(address_source)
            DBC_number_source, row_number_source = get_address(address_source)
            print('Source DBC No:', DBC_number_source)
            print('Source Row No:', row_number_source)

            # if instruction_line[0] == 'WRITE':
            #Calling read functionx
            param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, 'Read', 0, 511, None)
            perform_param['write'] += param_table['write']
            perform_param['TR_writes'] += param_table['TR_writes']
            perform_param['read'] += param_table['read']
            perform_param['TR_reads'] += param_table['TR_reads']
            perform_param['shift'] += param_table['shift']
            perform_param['STORE'] += param_table['STORE']

            data_hex = data[2:]
        else:
            data = instruction_line[2]
            data_hex = data[2:]

        # append trailing zeros
        if (len(data_hex) != 128):
        # mask data_hex with zeros:
            N = 128 - len(data_hex)
            data_hex = data_hex.ljust(N + len(data_hex), '0')

        # instructions for CPIM operations
        if instruction_line[0] == 'CPIM':
            if instruction_line[3] == 'COPY':
                # call Transverse Write
                param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0, 511, data_hex)

                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']

            elif instruction_line[3] == 'STORE':
                # call read and then write
                param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0, 511, data_hex)

                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += (param_table['STORE'] + 1)


            elif 'SHL' in instruction_line[3] or 'SHR' in instruction_line[3]:
                i = instruction_line[3]
                instruction = ''
                instruction = i[:3] + ' ' + i[3:]
                print(instruction)
                # call operations
                param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, instruction, 0, 511)
                data_hex = data[2:]
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']

                param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0, 511, data_hex)
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']

            elif instruction_line[3] == 'CARRY' or instruction_line[3] == 'CARRYPRIME':
                # call operations
                param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, instruction_line[3], 0, 511)
                data_hex = data[2:]
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']

                param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0, 511, data_hex)
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']

            elif instruction_line[3] == 'ADD':
                bit_no = instruction_line[4]
                # call operations
                param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, instruction_line[3], 0, instruction_line[4])
                data_hex = data[2:]
                total_energy += 512*(0.504676821+0.000958797)+512*0.1+(512-64)*0.1+(512-128)*0.1
                total_cycles += (8*((9+4+4)) + 8*(9+4+4+4) + 7*(9+4+4+4))
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']
                # print(perform_param)

                param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0, 511, data_hex)
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']

            elif instruction_line[3] == 'MULT':

                # shift A for length of A
                bit_no = int(instruction_line[4])

                for i in range(0, bit_no-1):
                    # Shift by 1 and write
                    instruction = 'SHR' + ' ' + '1'
                    # call operations
                    param_table, A = call_DBC(dbcs[15], i, instruction, 0, 511)
                    A_hex = A[2:]
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']

                    param_table = write_type(dbcs[15], i+1, 0, 0, 511, A_hex)
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']

                # Convert hex data to bin
                data_hex_size = int(bit_no/4)
                data_bin = (bin(int(data_hex, 16))[2:]).zfill(data_hex_size)

                # Read B(data_hex) bitwise and Mask shifted A with zeros.
                N = 128
                mask_zeros = ''
                mask_zeros = mask_zeros.ljust(N, '0')
                # print(len(mask_zeros))
                # print('data_bin[i]', type(data_bin[i]))

                for i in range(0, int(bit_no)):

                    if (int(data_bin[i]) == 0):
                        # print('mask with zeros')
                        param_table = write_type(dbcs[15], i, 0, 0, 511, mask_zeros)
                        perform_param['write'] += param_table['write']
                        perform_param['TR_writes'] += param_table['TR_writes']
                        perform_param['read'] += param_table['read']
                        perform_param['TR_reads'] += param_table['TR_reads']
                        perform_param['shift'] += param_table['shift']
                        perform_param['STORE'] += param_table['STORE']


                # call mult operations
                param_table, data = call_DBC(dbcs[15], 0, instruction_line[3], 0, instruction_line[4])
                data_hex = data[2:]
                total_energy += (512 * (0.504676821 + 0.000958797) + 512 * 0.1 + (512 - 64) * 0.1 + (512 - 128) * 0.1) +  512*(6*(0.3) + 8*(0.1) + 8*(0.7) + 8*(0.3) + 7*(0.3) + 3*(0.504676821) + 3*(0.1) + 2*(0.3) + 3*(0.7) + 3*(0.3) + 1*(0.3) + 4*(0.3) + 4*(0.7))
                total_cycles += (8*((9+4+4)) + 8*(9+4+4+4) + 7*(9+4+4+4)) + 6*(2) + 8*(9+4+4+4) + 8*(9+4+4) + 8*(2) + 7*(2) + 3*(9+4+4) + 3*(9+4+4+4) + 2*(2) + 3*(9+4+4) + 3*(9+4+4+4+2) + 1*(2) + 4*(9+4+4+4+2) + 4*(9+4+4)
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']

                param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0, 511, data_hex)
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']
            else:
                # call operations for logic operands
                param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, instruction_line[3], 0, 511)
                data_hex = data[2:]
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']

                # call write function:
                param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0, 511, data_hex)
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']

        elif  instruction_line[0] == 'SubByte':
            # read bits
            read_bits = ''
            for i in range(2,int(instruction_line[3]) + 2, 2):
                dec = (data_hex[i-2:i])
                dec = int(dec,16)
                sbox_val = SB.subBytes(dec)
                # convert to decimal number
                hex_data = hex(sbox_val)
                read_bits += (str(hex_data[2:]).zfill(2))
            # mask data_hex with zeros:
            N = 128 - len(read_bits)
            read_bits = read_bits.ljust(N + len(read_bits), '0')
            param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[4], 0, 4*int(instruction_line[3]), read_bits)

            perform_param['write'] += param_table['write']
            perform_param['TR_writes'] += param_table['TR_writes']
            perform_param['read'] += param_table['read']
            perform_param['TR_reads'] += param_table['TR_reads']
            perform_param['shift'] += param_table['shift']
            perform_param['STORE'] += param_table['STORE']

        # Close opened file
        instruction_file.close()

total_energy += perform_param['write'] * 512* 0.1
total_energy += perform_param['TR_writes'] * 0.3 *512
total_energy += perform_param['read'] * 0.7 * 512
total_energy += perform_param['TR_reads'] * 0.504676821*512
total_energy += perform_param['shift'] * 0.3 * 512
total_energy += perform_param['STORE'] * 0
total_energy += perform_param['TR_reads'] * 0.000958797 * 512 #TODO: check pim energy

total_cycles += perform_param['write'] * (9+4+4+4)
total_cycles += perform_param['TR_writes'] * (2+9+4+4+4)
total_cycles += perform_param['read'] * (9+4+4)
total_cycles += perform_param['TR_reads'] * (9+4+4)
total_cycles += perform_param['shift'] * 2
total_cycles += perform_param['STORE'] * (10) #TODO: check STORE cycles

print(perform_param)

print('The total_cycles and  total_energy is :',total_cycles,'and', total_energy)
