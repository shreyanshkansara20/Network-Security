#!/usr/bin/env python
# coding: utf-8

# Shreyansh Kansara

import sys


def caesar_str_enc(plaintext, K):
    ciphertext=""
    for ch in plaintext:
        encch = caesar_ch_enc(ch, K)
        ciphertext = ciphertext + encch
        
    return ciphertext

def caesar_ch_enc(ch, K):
    
    # everything needed to map a char to its encoded char with K as the parameter
    ch=ch.lower()
    ch_int=ord(ch)
    K=int(K)%26
    
    if ch_int >=97 and ch_int <=122:
        enc_int=ch_int+K
        if enc_int > 122:
            enc_int=enc_int-26
    else:
        return ch
    
    encch=chr(enc_int)
        
    
    return encch
    

def caesar_str_dec(ciphertext, K):
    plaintext = ""
    for ch in ciphertext:
        decch = caesar_ch_dec(ch, K)
        plaintext = plaintext + decch
        
    return plaintext

def caesar_ch_dec (ch, K):
    
    # ...
    ch_int=ord(ch)
    K=int(K)%26
    
    if ch_int >=97 and ch_int <=122:
        dec_int=ch_int-K
        if dec_int < 97:
            dec_int=dec_int+26
    else:
        return ch
    
    decch=chr(dec_int)
    
    
    return decch


def test_module():
    K = sys.argv[1]
    input_str = sys.argv[2]
    
  
    encstr = caesar_str_enc(input_str, K)
    print(encstr)
    decstr = caesar_str_dec(encstr, K)
    print(decstr)
    
   
if __name__=="__main__":
    test_module()




