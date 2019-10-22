#!/usr/bin/python

from bitarray import bitarray



def padding(msg):
    a = bitarray(endian='big')
    a.frombytes(msg.encode('ascii'))
    while len(a) % 64 != 0:
        a.append(0)

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

IP = [

      58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7
]

IP_inverse = [

            40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25

        ]

E_e = [
    32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1
     ]




S_BOX = [
         
[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
 [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
 [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
 [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
],

[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
 [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
 [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
 [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
],

[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
 [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
 [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
 [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
],

[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
 [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
 [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
 [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
],  

[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
 [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
 [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
 [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
], 

[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
 [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
 [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
 [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
], 

[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
 [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
 [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
 [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
],
   
[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
 [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
 [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
 [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
]
]



P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]
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

def f(block,key):

    ready_for_sbox = E(block) ^ key

    # do the substitution
    sublocks = [None] * 8
    aux = bitarray(endian='little')
    j = 0
    for k in range(0,len(ready_for_sbox),6):
        sublocks[j] = ready_for_sbox[k:k+6]
        j = j + 1

    for i in range(len(sublocks)):
        chunk = sublocks[i]
        row = onethree(chunk[0],chunk[len(chunk) - 1])
        column = onefifteen(chunk[1],chunk[2],chunk[3],chunk[4])
        output_value = decimalToBinary(S_BOX[i][row][column])
        aux.extend(output_value)



    result = bitarray('0'*32,endian='little')
    k = 0    
    for x in P:
        result[k] = aux[x - 1]
        k = k + 1

    return result


   

def decimalToBinary(n): 
    return (bin(n).replace("0b","")).zfill(4)





def onethree(first,second):
    if first == False and second == False:
        return 0
    if first == False and second == True:
        return 1
    if first == True and second == False:   
        return 2
    if first == True and second == True:
        return 3


def onefifteen(first,second,third,fourth):
    if first == False and second == False and third == False and fourth == False:
        return 0
    if first == False and second == False and third == False and fourth == True:
        return 1
    if first == False and second == False and third == True and  fourth == False:
        return 2
    if first == False and second == False and third == True and  fourth == True:
        return 3
    if first == False and second == True and third == False and  fourth == False:
        return 4
    if first == False and second == True and third == False and  fourth == True:
        return 5
    if first == False and second == True and third == True and  fourth == False:
        return 6
    if first == False and second == True and third == True and  fourth == True:
        return 7
    if first == True and second == False and third == False and  fourth == False:
        return 8   
    if first == True and second == False and third == False and  fourth == True:
        return 9
    if first == True and second == False and third == True and  fourth == False:
        return 10
    if first == True and second == False and third == True and  fourth == True:
        return 11
    if first == True and second == True and third == False and  fourth == False:
        return 12
    if first == True and second == True and third == False and  fourth == True:
        return 13
    if first == True and second == True and third == True and  fourth == False:
        return 14 
    if first == True and second == True and third == True and  fourth == True:
        return 15     







def E(input_array):
    counter = 0
    result = bitarray('0'*48,endian='little')
    for expand in E_e:
        result[counter] = input_array[expand - 1]
        counter = counter + 1  
    return result

def DES_ENCRYPT(msg):

    msg = padding(msg)
    ip_aux = bitarray('0'*len(msg),endian='little')
    ip_reverse_aux = bitarray('0'*len(msg),endian='little')
    result = bitarray('0'*len(msg),endian='little')
    counter = 0
    L = [None] * 32
    R = [None] * 32

    for ip in IP:
        ip_aux[counter] = msg[ip - 1]
        counter = counter + 1
    
    
    L[0] = ip_aux[0:32]
    R[0] = ip_aux[32:64]

    # 16 ROUNDS, this is where the magic happend

    for i in range(1,17):
        L[i] = R[i - 1]
        R[i] = L[i - 1] ^ f(R[i - 1],key_SCHEDULE(i - 1))
    

    result = L[16].copy()
    result.extend(R[16])

    counter = 0
    for reverse_ip in IP_inverse:
        ip_reverse_aux[counter] = result[reverse_ip - 1]
        counter = counter + 1

    
    return result


print(DES_ENCRYPT('vggfrfr'))


