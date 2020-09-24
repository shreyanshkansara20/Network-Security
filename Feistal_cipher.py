#!/usr/bin/env python
# coding: utf-8

# # Feistel Cipher

# Shreyansh Kansara

# bitwise XOR function operating on two byte sequences (multiple Bytes each)
# If the argument have different number of bytes, it will return a result that 
# is as long as the shorter argument. 
import random
def xor(byteseq1, byteseq2):
    # First we convert each byte to its int value
    l1 = [b for b in byteseq1]
    l2 = [b for b in byteseq2]

    # Then we use the xor ^ operator to xor the integer values
    # At the same time, we convert the resulting intergers back to byte form
    # Note that the zip function automatically picks the size of the shorter of l1,l2
    # so l1xorl2 is the same size as the shorter of l1 and l2. This allows us to 
    # select our F function to always give a long output even if we need part of it.
    l1xorl2 = [bytes([elem1^elem2]) for elem1,elem2 in zip(l1,l2)]
    
    # finally, we convert the list of individual XOR results into a byte sequence
    # by concatenating all of them together
    result = b''.join(l1xorl2)

    return result

# As discussed, round function F can be any arbitrary function but it's usually a shuffling function
# such as a hash function. Here we use the SHA1 hash (we'll study the details of it later)
# to create a function that returns a 32bit string (since we assume 32 bit byteseq input)
def F(byteseq, k):
    import hmac, hashlib
    
    # create a hmac sha1 
    h = hmac.new(k, byteseq, hashlib.sha1)
    # Return first 8 bytes of the calculated hmac sha1 hash
    return h.digest()[:8]

# main block processing
def feistel_block(LE_inp, RE_inp, k):
    
    # LEinp and REinp are the outputs of the previous round
    # k is the key for this round which usually has a different 
    # value for different rounds
    
    LE_out = RE_inp
    RE_out = xor(LE_inp,F(RE_inp,k))
    
    
    return LE_out, RE_out
    

# In a real Feistel implementation, different keys are used in different rounds. Here
# we use 64bit keys so for 16 rounds, we need 16 random 8byte keys. We can just generate
# 16 random 8 byte numbers we use the random.randint() function to be able to set the seed
# value and create the same keys for both the encoder and the decoder
def gen_keylist(keylenbytes, numkeys, seed):
    
    # We need to generate numkeys keys each being keylen bytes long
    keylist = []
    random.seed(seed)
    
    # Use the random.randint(min,max) function to generate individual
    # random integers in range [min, max]. Generate a list of 16
    # random byte sequences each of the 4 bytes long to be used as 
    # keys for 16 stages of the feistel encoder. To make sure we have control over
    # the generated random numbers meaning that the same sequence is 
    # generated in different runs of our program, 
    
    # keylist = [16 elements of 'bytes' type and 4 bytes long each]
    for i in range(0,numkeys):
        mid_key=[]
        for j in range(keylenbytes):
            mid_gen=random.randint(0,255)
            mid_key.append(mid_gen.to_bytes(1,'big'))
        byte_key=b''.join(mid_key)    
        keylist.append(byte_key)
    
    
    
    return keylist


def feistel_enc(inputblock, num_rounds, seed):
    # This is the function that accepts one bloc of plaintext
    # and applies all rounds of the feistel cipher and returns the
    # cipher text block. 
    # Inputs:
    # inputblock: byte sequence representing input block
    # num_rounds: integer representing number of rounds in the feistel 
    # seed: integer to set the random number generator to defined state
    # Output:
    # cipherblock: byte sequence
    
    # first generate the required keys
    keylist = gen_keylist(4, num_rounds, seed)
    
    L=inputblock[:4]
    R=inputblock[4:]
    
   
    #print(len(L),len(R))
    for i in range(0,num_rounds):
        L,R=feistel_block(L,R,keylist[i])
        
   
    cipherblock=R+L
    
    
    
    return cipherblock

    
def feistel_enc_test(input_fname, seed, num_rounds, output_fname):
    
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

    
    
    # Loop over al blocks and use the feistel_enc to generate the cipher block
    # append all cipherblocks together to form the outut byte sequence
    # cipherbyteseq = b''.join([list of cipher blocks])
    
    cipher=[]
    for i in inputblock:
        cipher.append(feistel_enc(i,num_rounds,seed))
    
    
    cipherbyteseq=b''.join(cipher)
    
    
    
    
    # write the cipherbyteseq to output file
    fout = open(output_fname, 'wb')
    fout.write(cipherbyteseq)
    fout.close()
    
    
def feistel_dec(inputblock, num_rounds, seed):
    # This is the function that accepts one bloc of ciphertext
    # and applies all rounds of the feistel cipher decruption and returns the
    # plain text block. 
    # Inputs:
    # inputblock: byte sequence representing input block
    # num_rounds: integer representing number of rounds in the feistel 
    # seed: integer to set the random number generator to defined state
    # Output:
    # cipherblock: byte sequence
    
    # first generate the required keys
    keylist = gen_keylist(4, num_rounds, seed)
    
    L=inputblock[:4]
    R=inputblock[4:]
    

    
    for i in range(0,num_rounds):
        L, R=feistel_block(L,R,keylist[num_rounds-1-i])

   
    plainblock=R+L
    
    
    
    return plainblock

def feistel_dec_test(input_fname, seed, num_rounds, output_fname):
    
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
    inputblock.append(inpbyteseq[j:len(inpbyteseq)])

    
    last_ele_length=len(inputblock[-1])
    
    if last_ele_length < 8:
        x=b'\x20'*(8-last_ele_length)
        inputblock[-1]+=x

    
    
    # Loop over al blocks and use the feistel_dec to generate the plaintext block
    # append all plainblocks together to form the output byte sequence
    # plainbyteseq = b''.join([list of plain blocks])
    
    plain=[]
    for i in inputblock:
        plain.append(feistel_dec(i,num_rounds,seed))
    
    plainbyteseq=b''.join(plain)
    

    
    # write the plainbyteseq to output file
    fout = open(output_fname, 'wb')
    fout.write(plainbyteseq)
    fout.close()
    


