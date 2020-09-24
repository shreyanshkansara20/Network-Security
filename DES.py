#!/usr/bin/env python
# coding: utf-8

# Shreyansh Kansara




# Given the above transformations, we can define all types of transformation utility functions
# for example a function to convert a given byte sequence to a string representation of bits
def byteseq2binstr(byteseq):
    # first convert to a list string binary representations of each byte
    bitslist2 = [bin(int(b))[2:].zfill(8) for b in byteseq]
    
    # then merge all those strings
    allbitsstr = ''.join(bitslist2)
    
    return allbitsstr



# Initial Permutation and inverse permutaion operatoins can be easily performed 
# using lists and proper indexing of the elements of the lists in Python 

# Let's define the order of the elements at the output of the Initial Permutation (IP) stage
# in the following list (we subtract the values in the book by 1 since we always
# index array elements from 0 upward) 
BookInitPermOrder = [58,50,42,34,26,18,10,2,
                   60,52,44,36,28,20,12,4,
                   62,54,46,38,30,22,14,6,
                   64,56,48,40,32,24,16,8,
                   57,49,41,33,25,17,9,1,
                   59,51,43,35,27,19,11,3,
                   61,53,45,37,29,21,13,5,
                   63,55,47,39,31,23,15,7]

InitPermOrder = [x-1 for x in BookInitPermOrder]

# Same can be done for Inverse Initial Permuation
BookInvInitPermOrder = [40,8,48,16,56,24,64,32,
                        39,7,47,15,55,23,63,31,
                        38,6,46,14,54,22,62,30,
                        37,5,45,13,53,21,61,29,
                        36,4,44,12,52,20,60,28,
                        35,3,43,11,51,19,59,27,
                        34,2,42,10,50,18,58,26,
                        33,1,41,9,49,17,57,25]

InvInitPermOrder = [x-1 for x in BookInvInitPermOrder]


permute = [16,7,20,21,29,12,28,17,
            1,15,23,26,5,18,31,10,
            2,8,24,14,32,27,3,9,
            19,13,30,6,22,11,4,25]

# Now you can put the above inside this function so that it can be called to perform
# both initial and inverse initial permutations for DES
# You may need some conversion from byteseq to bitstring and reverse to use this function with your
# feistel implementation
def Permutation(bitstr, permorderlist):
    mid_permedbitstr = [bitstr[b-1] for b in permorderlist]
    permedbitstr=''.join(mid_permedbitstr)
    
    #....
    
    return permedbitstr






# EXPANSION (E)
# The E operation involves inserting additional bits inside the input 32 bits sequence
# We can start with an empty output bit string and then take proper bits from the input 
# according to the E_TABLE below and add the bits one by one to the end of the output
# string

E_TABLE = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,
16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]

def Expansion(inputbitstr32, e_table):
    # the input string is 32 bits long and the output string will be 48 bits long or
    # to be more exact, it will be as long as the e_table (which is 48 bits for DES)
    
    # create output empty string
    mid_output=[inputbitstr32[b-1] for b in e_table]
    outputbitstr48 = ''.join(mid_output)

    # add proper elements from the inputbitstr32 according to the e_table
    
    return outputbitstr48



# XOR
# In Feistel, we implemented XOR function with byte sequences as input. Here we redefine the XOR function
# to operate on bit string inputs.

def XORbits(bitstr1,bitstr2):
    # Both bit strings should be the same length
    # output will be a string with the same length
    xor_result = int(bitstr1,2) ^ int(bitstr2,2)
   
    xor_result=bin(xor_result)[2:].zfill(len(bitstr1))
    
    return xor_result



# We previously showed how to extract the bits from 6bit blocks and find the row and column indices for
# use in the s-box operation. Each S-box can be represented as a list of lists to allow row-column access
# and we can put all s-boxes in a parent list SBOX for easy addressing. Remember that Sbox-1 is SBOX[0]
# and sbox-2 is SBOX[1] and sbox-8 is SBOX[7]

SBOX = [
# Box-1
[
[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
],
# Box-2

[
[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
[0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
],

# Box-3

[
[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]

],

# Box-4
[
[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
],

# Box-5
[
[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
],
# Box-6

[
[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]

],
# Box-7
[
[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
],
# Box-8

[
[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
]

]

# Let's define a table for quick conversion of sbox decimals to 4 bit binary
DECtoBIN4 = {0: '0000',
            1: '0001',
            2: '0010',
            3: '0011',
            4: '0100',
            5: '0101',
            6: '0110',
            7: '0111',
            8: '1000',
            9: '1001',
            10: '1010',
            11: '1011',
            12: '1100',
            13: '1101',
            14: '1110',
            15: '1111'}




# In[50]:


# we can now implement the sbox operations by combining the above material


def sbox_lookup(input6bitstr, sboxindex):
    # find the row index (0-3)
    # find the col index (0-7)
    row = int(input6bitstr[0]+input6bitstr[5],base=2)
    col = int(input6bitstr[1:5],base=2)
    sbox_value = SBOX[sboxindex][row][col]
    
    # Need to convert to 4 bits binary string    
    return DECtoBIN4[sbox_value]


# ## The Round Function F()
# 
# ##### Having all above function implemented and tested, the round function will be easy to implement.




def functionF(bitstr32, keybitstr48):
    
    expanded_string=Expansion(bitstr32,E_TABLE)
   
    xored_string=XORbits(expanded_string,keybitstr48)
   
    S_box_input=[xored_string[i:i+6] for i in range(0,len(xored_string), 6)]
   
    S_box_output=[sbox_lookup(S_box_input[j],j) for j in range(len(SBOX))]
    S_box_output=''.join(S_box_output)
    
    outbitstr32=Permutation(S_box_output,permute)
    
    # return the result
    return outbitstr32




# ## DES Encryption



def byteseq2binstr(byteseq):
    # first convert to a list string binary representations of each byte
    bitslist2 = [bin(int(b))[2:].zfill(8) for b in byteseq]
    
    # then merge all those strings
    allbitsstr = ''.join(bitslist2)
    
    return allbitsstr

PC_1=[57,49,41,33,25,17,9,
        1,58,50,42,34,26,18,
        10,2,59,51,43,35,27,
        19,11,3,60,52,44,36,
        63,55,47,39,31,23,15,
        7,62,54,46,38,30,22,
        14,6,61,53,45,37,29,
        21,13,5,28,20,12,4]

PC_2=[14,17,11,24,1,5,
    3,28,15,6,21,10,
    23,19,12,4,26,8,
    16,7,27,20,13,2,
    41,52,31,37,47,55,
    30,40,51,45,33,48,
    44,49,39,56,34,53,
    46,42,50,36,29,32]

Bit_rotation=[1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

def des_keygen(C_inp, D_inp, roundindex):
    C_out = C_inp[Bit_rotation[roundindex]:]+C_inp[:Bit_rotation[roundindex]]
    D_out = D_inp[Bit_rotation[roundindex]:]+D_inp[:Bit_rotation[roundindex]]
    
    PC_2_inp = C_out+D_out
    
    PC_2_out=[PC_2_inp[b-1] for b in PC_2]
    key48=''.join(PC_2_out)
    
    return key48, C_out, D_out
 
def des_round(LE_inp32, RE_inp32, key48):
    # LEinp and REinp are the outputs of the previous round
    # k is the key for this round which usually has a different 
    # value for different rounds
    LE_out32=RE_inp32
    RE_out32=XORbits(functionF(RE_inp32,key48),LE_inp32)

    
    return LE_out32, RE_out32

# even though DES is strictly 16 rounds, we keep the number of rounds as a parameter for
# easier extension and also for better testing (setting rounds to 1).

def des_enc(inputblock, num_rounds, inputkey64):
    # This is the function that accepts one bloc of plaintext
    # and applies all rounds of the DES cipher and returns the
    # cipher text block. 
    # Inputs:
    # inputblock: byte sequence representing input block
    # num_rounds: integer representing number of rounds in the feistel 
    # key: byte sequence (8 bytes)
    # Output:
    # cipherblock: byte sequence
    
    input_string = byteseq2binstr(inputblock)
    
    InitPermOrder = [input_string[x-1] for x in BookInitPermOrder]
    des_inp=''.join(InitPermOrder)
    
    LE_out32=des_inp[:32]
    RE_out32=des_inp[32:]
    
    input_key = byteseq2binstr(inputkey64)
    
    keygen_inp=[input_key[k-1] for k in PC_1]
    keygen_inp=''.join(keygen_inp)
    
    C_out=keygen_inp[:28]
    D_out=keygen_inp[28:]
    #key_list=[]
    
    for i in range(num_rounds):
        key,C_out,D_out=des_keygen(C_out,D_out,i)
        LE_out32,RE_out32=des_round(LE_out32,RE_out32,key)
    
    cipherblock_mid=RE_out32+LE_out32
    
    InvInitPermOrder = [cipherblock_mid[x-1] for x in BookInvInitPermOrder]
    
    cipherblock=''.join(InvInitPermOrder)
    
    
        
    cipherblock=int(cipherblock, 2).to_bytes(len(cipherblock) // 8, byteorder='big')
    #Reference taken from https://stackoverflow.com/questions/32675679/convert-binary-string-to-bytearray-in-python-3
    
    return cipherblock
    
def des_enc_test(input_fname, inputkey64, num_rounds, output_fname):
    
    # inputkey64: byte sequence (8 bytes)
    # numrounds: asked since your feistel already has it but we always use 16 for DES
    
    # First read the contents of the input file as a byte sequence
    finp = open(input_fname, 'rb')
    inpbyteseq = finp.read()
    finp.close()
    
    # Then break the inpbyteseq into blocks of 8 bytes long and 
    # put them in a list
    # Pad the last element with spaces b'\x20' until it is 8 bytes long
    # blocklist = [list of 8 byte long blocks]
    
    inputblock=[]
    j=0
    for i in range(0,len(inpbyteseq)-1):
        if (j+8) < len(inpbyteseq)-1:
            inputblock.append(inpbyteseq[j:j+8])
            j+=8
        else:
            break
    inputblock.append(inpbyteseq[j:len(inpbyteseq)-1])

    
    last_ele_length=len(inputblock[-1])
    
    if last_ele_length < 8:
        x=b'\x20'*(8-last_ele_length)
        inputblock[-1]+=x

    
    # Loop over al blocks and use the dec_enc to generate the cipher block
    # append all cipherblocks together to form the outut byte sequence
    # cipherbyteseq = b''.join([list of cipher blocks])
    
    cipher=[]
    for i in inputblock:
        cipher.append(des_enc(i,num_rounds,inputkey64))
    
    
    cipherbyteseq=b''.join(cipher)
    
    # write the cipherbyteseq to output file
    fout = open(output_fname, 'wb')
    fout.write(cipherbyteseq)
    fout.close()
    

    


# ## DES Decryption

# In[47]:



def des_dec(inputblock, num_rounds, inputkey64):
    # This is the function that accepts one bloc of ciphertext
    # and applies all rounds of the DES cipher and returns the
    # plaintext text block. 
    # Inputs:
    # inputblock: byte sequence representing ciphertext block
    # num_rounds: integer representing number of rounds in the feistel 
    # key: byte sequence (8 bytes)
    # Output:
    # plainblock: byte sequence
    
    input_string = byteseq2binstr(inputblock)
    
    InitPermOrder = [input_string[x-1] for x in BookInitPermOrder]
    des_inp=''.join(InitPermOrder)
    
    LE_out32=des_inp[:32]
    RE_out32=des_inp[32:]
    
    input_key = byteseq2binstr(inputkey64)
    
    keygen_inp=[input_key[k-1] for k in PC_1]
    keygen_inp=''.join(keygen_inp)
    
    C_out=keygen_inp[:28]
    D_out=keygen_inp[28:]
    key_list=[]
    
    for i in range(num_rounds):
        key,C_out,D_out=des_keygen(C_out,D_out,i)
        key_list.append(key)
    for j in range(num_rounds):
        LE_out32,RE_out32=des_round(LE_out32,RE_out32,key_list[num_rounds-j-1])
    
    plaintext_mid=RE_out32+LE_out32
    
    InvInitPermOrder = [plaintext_mid[x-1] for x in BookInvInitPermOrder]
    
    plaintext=''.join(InvInitPermOrder)
    
    
        
    plainblock=int(plaintext, 2).to_bytes(len(plaintext) // 8, byteorder='big')
    
    #Reference taken from https://stackoverflow.com/questions/32675679/convert-binary-string-to-bytearray-in-python-3
    
    return plainblock
    
def des_dec_test(input_fname, inputkey64, num_rounds, output_fname):
    
    # inputkey64: byte sequence (8 bytes)
    # numrounds: asked since your feistel already has it but we always use 16 for DES
        
    # First read the contents of the input file as a byte sequence
    finp = open(input_fname, 'rb')
    cipherbyteseq = finp.read()
    finp.close()
    
    # do the decryption rounds
    inputblock=[]
    j=0
    for i in range(0,len(cipherbyteseq)-1):
        if (j+8) < len(cipherbyteseq)-1:
            inputblock.append(cipherbyteseq[j:j+8])
            j+=8
        else:
            break
    inputblock.append(cipherbyteseq[j:len(cipherbyteseq)])

        
        
    plain=[]
    for i in inputblock:
        plain.append(des_dec(i,num_rounds,inputkey64))
    
    plainbyteseq=b''.join(plain)

    # write the plainbyteseq to output file
    fout = open(output_fname, 'wb')
    fout.write(plainbyteseq)
    fout.close()



    

    

