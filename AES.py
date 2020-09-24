#!/usr/bin/env python
# coding: utf-8

# Shreyansh Kansara


from Crypto.Cipher import AES


# In[12]:


def byteseq2binstr(byteseq):
    # first convert to a list string binary representations of each byte
    bitslist2 = [bin(int(b))[2:].zfill(8) for b in byteseq]
    
    # then merge all those strings
    allbitsstr = ''.join(bitslist2)
    
    return allbitsstr
    


# In[13]:


def aes_enc(inputblock,key):
    #data=bytes.fromhex(inputblock)
    #key_bytes=bytes.fromhex(key)
    cipher=AES.new(key,AES.MODE_ECB)
    ct_bytes=cipher.encrypt(inputblock)
    return ct_bytes
    


# In[14]:


def invertbit(inputblock,b):
    #data=bytes.fromhex(inputblock)
    bitseq=byteseq2binstr(inputblock)
    #print(bitseq)
    if bitseq[b] == '0':
        seq_list=list(bitseq)
        seq_list[b]='1'
        bitseq=''.join(seq_list)
        #print(bitseq)
    else:
        seq_list=list(bitseq)
        seq_list[b]='0'
        bitseq=''.join(seq_list)
        #print(bitseq)
        
    new_input=int(bitseq, 2).to_bytes(len(bitseq) // 8, byteorder='big')
    #print(new_input)
    return new_input


# In[15]:


def findbitdiff(origin_cipher,new_cipher):
    #origin_cipher=bytes.fromhex(origin_cipher)
    #new_cipher=bytes.fromhex(new_cipher)
    origin_cipher_bitseq=byteseq2binstr(origin_cipher)
    #print(origin_cipher_bitseq)
    new_cipher_bitseq=byteseq2binstr(new_cipher)
    #print(new_cipher_bitseq)
    count=0
    for i in range(len(origin_cipher_bitseq)):
        if origin_cipher_bitseq[i]!=new_cipher_bitseq[i]:
            count+=1
    return count


# In[16]:


# Homework 5
# Testing the avalanche properties of AES using an automated code

# Write a function to test the avalanche property of AES when different single bits of 
# the inputblock are inverted. 

# In this experiment you receive an initial inputblock and key to perform AES encryption and
# find the cipherblock. Then you will use the bitlist provided as the 3rd input to the function
# to decide which bit of the inputblock to invert in additional experiments and then perform the
# AES encryption again on the modified input (with only one bit difference to original input)
# Then you compare the ciphertext for each additional experiment with the ciphertext of the
# original experiment and count the number of bits that are different between them.

# The output of your function will be the list of the number-of-differences from all experiments

# Make sure you test your code before submission by setting the bitlist to [7] and comparing the results 
# with Table 6.5 and Table 6.6 of the textbook. you can also try inverting other bit values manually and generate 
# ciphers using the AES example we did in the class and compare with the output of your function.

# As usual, we will import your submitted python file in another script and just call the aes_input_av_test() and
# aes_key_av_test() functions and check the output list of each function. It's ok if you have other utility functions
# in your submission and they will not be called or tested.


def aes_input_av_test(inputblock, key, bitlist):
    # inputblock and key are 16 byte values each
    # bitlist is a list of integers that define the position of the
    # bit in the inputblock that needs to be inverted, one at a time, for example
    # [0, 3, 6, 25, 78, 127]
    
    # 1- any initializations necessary
    diff_list = []
    
    # 2- perform encryption of the original values
    #    anyway you like. It doesn't have to be with 
    #    with this exact function form
    originalcipher = aes_enc(inputblock, key)
    
    # 3- for every value given in the bitlist:
    for b in bitlist:
        #invert the value of the corresponding bit in the inputblock (doesn't have to be in this exact
        # function form)
        newinput = invertbit(inputblock, b)
        
        # perform encryption
        newcipher = aes_enc(newinput, key)
        
        # find the number of bit differences between the two ciphertexts (doesn't have to be exactly in
        # this function form)
        # Use any method you like to find the difference. 
        numbitdifferences = findbitdiff (originalcipher, newcipher)
        
        # add it to the list
        diff_list.append(numbitdifferences)
        
    # return the list of numbers
    return diff_list


# We also perform similar experiment by keeping the inputblocl fixed and changing the
# selected bits of the key
def aes_key_av_test(inputblock, key, bitlist):
    # inputblock and key are 16 byte values each
    # bitlist is a list of integers that define the position of the
    # bit in the key that needs to be inverted, one at a time, for example
    # [0, 3, 6, 25, 78, 127]
    
    # 1- any initializations necessary
    diff_list = []
    
    # 2- perform encryption of the original values
    #    anyway you like. It doesn't have to be with 
    #    with this exact function form
    originalcipher = aes_enc(inputblock, key)
    
    # 3- for every value given in the bitlist:
    for b in bitlist:
        #invert the value of the corresponding bit in the key (doesn't have to be in this exact
        # function form)
        newkey = invertbit(key, b)
        
        # perform encryption
        newcipher = aes_enc(inputblock, newkey)
        
        # find the number of bit differences between the two ciphertexts (doesn't have to be exactly in
        # this function form)
        numbitdifferences = findbitdiff (originalcipher, newcipher)
        
        # add it to the list
        diff_list.append(numbitdifferences)
        
    # return the list of numbers
    return diff_list


    
    
    



#print(aes_input_av_test(b"\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10",b"\x0f\x15\x71\xc9\x47\xd9\xe8\x59\x0c\xb7\xad\xd6\xaf\x7f\x67\x98",[0, 7, 6, 25, 78, 127]))

#print(aes_key_av_test(b"\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10",b"\x0f\x15\x71\xc9\x47\xd9\xe8\x59\x0c\xb7\xad\xd6\xaf\x7f\x67\x98",[0, 7, 6, 25, 78, 127]))




#print(aes_key_av_test(b"\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10",b"\x0f\x15\x71\xc9\x47\xd9\xe8\x59\x0c\xb7\xad\xd6\xaf\x7f\x67\x98",[0, 7, 6, 25, 78, 127]))

