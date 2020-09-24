#!/usr/bin/env python
# coding: utf-8

# Shreyansh Kansara

# Vigenere encryption function
def vigenere_enc(keyword, plaintext):
    # keyword is a string of arbitrary length
    # plaintext is the plaintext string of arbitrary length
    # Both strings will be from {a,b,...,z}
    
    # perform the encryption of given plaintext using the given keyword
    # according to the Vigenere cipher. You need to repeat the keyword 
    # enough times if needed to make it the same length as plaintext
    
    # c will be the resulting ciphertext
    #c = ...
    dic={}
    k=0
    for i in range(97,123):
        dic[chr(i)]=k
        k+=1
    
    plaintext=plaintext.lower()
    
    k_list=list(keyword.replace(" ",""))
    
    j=0
    c_list=[]
    for i in plaintext:
        if j >= len(k_list):
            j=0
        
        if ord(i) >=97 and ord(i) <=122:
            cipher_int=(dic[i]+dic[k_list[j]])%26
            j+=1
            c_list.append(list(dic.keys())[list(dic.values()).index(cipher_int)])
        else:
            c_list.append(i)
    
    c=''.join(c_list)
    return c


# Vionegere decryption function
def vigenere_dec(keyword, ciphertext):
    # keyword is a string of arbitrary length
    # ciphertext is the ciphertext string of arbitrary length
    # Both strings will be from {a,b,...,z}
    
    # perform the decryption of given ciphertext using the given keyword
    # according to the Vigenere cipher. You need to repeat the keyword 
    # enough times if needed to make it the same length as ciphertext
    
    # p will be the resulting plaintext
    # p = ...
    
    dic={}
    k=0
    for i in range(97,123):
        dic[chr(i)]=k
        k+=1
        
        
    ciphertext=ciphertext.lower()
    
    k_list=list(keyword.replace(" ",""))
    
    j=0
    dec_list=[]
    for i in ciphertext:
        if j >= len(k_list):
            j=0
        
        if ord(i) >=97 and ord(i) <=122:
            decipher_int=(dic[i]-dic[k_list[j]])%26
            j+=1
            if decipher_int < 0:
                decipher_int+=26
            
            dec_list.append(list(dic.keys())[list(dic.values()).index(decipher_int)])
        else:
            dec_list.append(i)
    
    p=''.join(dec_list)
    
    
    return p
    





#Usage : print(vigenere_enc("abcd","abcd"))
