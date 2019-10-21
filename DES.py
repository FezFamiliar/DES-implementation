#!/usr/bin/python

from bitarray import bitarray
import struct





def padding(msg):
    a = bitarray(endian='big')
    a.frombytes(msg.encode('ascii'))
    while len(a) % 64 != 0:
        a.append(0)

    print(len(a))
    return a

def left_rotate(value,amount):
    aux = value[0:amount]
    return value[amount:] + aux


PC_1 = [

    57, 49, 41, 33, 25, 17, 9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12, 4 
    
    ]

PC_2 = [
    14, 17, 11, 24, 1, 5,
     3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32

]


def key_SCHEDULE(key_index):
    key = bitarray(endian='big')
    key.frombytes(b'ffffffff')
    
    C = [None] * 16
    D = [None] * 16
    K = [None] * 16
    counter = 0
    for PC_1_bits in PC_1:
        get_value = key[PC_1_bits]
        key[counter] = get_value
        counter = counter + 1


    for drop_bit in range(len(key) - 1,0,-8):
        key.pop(drop_bit)


    C[0] = key[0:28]
    D[0] = key[28:56]

    for i in range(1,16):
        if i == 1 or i == 2 or i == 9 or i == 16:
            C[i] = left_rotate(C[i - 1],1)
            D[i] = left_rotate(D[i - 1],1)
        else:  
            C[i] = left_rotate(C[i - 1],2)
            D[i] = left_rotate(D[i - 1],2)



    
    
    ignore_bits = [54,43,38,35,25,22,18,9]
    for i in range(16):

        K[i] = C[i] + D[i]
        counter = 0

        for PC_2_bits in PC_2:                    
            get_value = K[i][PC_2_bits - 1]
            K[i][counter] = get_value
            counter = counter + 1


        for x in ignore_bits:
            K[i].pop(x)
        
    return K[key_index]



print(key_SCHEDULE(2))




