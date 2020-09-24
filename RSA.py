#!/usr/bin/env python
# coding: utf-8

# Shreyansh Kansara

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


# In[28]:


def importkeys(id_rsa_filename):
    # This function receives the full path of the id_rsa file as a string (including the file name itself) and
    # import the key information and returns the keypair
    # example 'c:/myfolder/id_rsa' (using forward '/' helps avoid some string issues)
    
    # return the complete keypair in the keypair format used in Crypto RSA module.
    f = open(id_rsa_filename,'r')
    keypair = RSA.importKey(f.read())
    
    return keypair

def rsa_enc_public(inputblock, keypair):
    # inputblock is a plaintext defined as a byte sequence
    # ciphertext is the encrypted data as byte sequence encrypted using the public key
    pubKey = keypair.publickey()
    encryptor = PKCS1_v1_5.new(pubKey)
    ciphertext = encryptor.encrypt(inputblock)
    
    return ciphertext

# def rsa_enc_private(inputblock, keypair):
#     # inputblock is a plaintext defined as a byte sequence
#     # ciphertext is the encrypted data as byte sequence encrypted using the private key
    
#     return ciphertext

# def rsa_dec_public(cipherblock, keypair):
#     # cipherblock is a given ciphertext defined as a byte sequence
#     # plaintext is the decrypted data as byte sequence decrypted using the public key
    
#     return plaintext

def rsa_dec_private(cipherblock, keypair):
    # cipherblock is a given ciphertext defined as a byte sequence
    # plaintext is the decrypted data as byte sequence decrypted using the private key
    decryptor = PKCS1_v1_5.new(keypair)
    plaintext = decryptor.decrypt(cipherblock, None)
    
    return plaintext

    



