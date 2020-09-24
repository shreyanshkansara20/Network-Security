#!/usr/bin/env python
# coding: utf-8

#Shreyansh Kansara

#Hill Cipher

def matrixinvmod26(M):
    import sys
    import numpy as np
    # Both the input argument M an doutput Minv26 are in the list of lists format i.e.,
    # [[M11,M12,M13],[M21,M22,M23],[M31,M32,M33]]
    # use np.array() and tolist() functions as described above for conversion between matrix and list-of-lists 
    # Calculate Minv26
    Mod26invTable = {}
    for m in range(26):
        for n in range(26):
            if (m*n)%26==1:
                Mod26invTable[m] = n
    
    
    
    M=np.array(M)
    Minv = np.linalg.inv(M)
    Mdet = int(np.linalg.det(M))
    
# Let's find Mdet26 and Mdetinv26
    Mdet26 = Mdet%26
    if Mdet26 in Mod26invTable:
        Mdetinv26 = Mod26invTable[Mdet26]
    else:
        Mdetinv26 = None # This should be an exit point since we can't find an inverse for M in mod-26
        print('Matrix is not Invertible! Please provide Invertible Matrix!')
        sys.exit()
    
#print(Mdet,Mdetinv26)

# Now, Let's find Madj26
    Madj = Mdet*Minv
    Madj26 = Madj%26


#print(np.matmul(M,Minv))

#So, The mod-26 inverse of M from equation (1) will be
    Minv26 = (Mdetinv26*Madj26)%26
    Minv26 = np.matrix.round(Minv26, 0)%26
    
    return Minv26

# 2- write the Hill encryption function 
def hill_enc(M, plaintext):
    import numpy as np
    # M is the encryption matrix - Let's assume it's always 3x3 for now
    # M is in the list of lists format i.e.,
    # [[M11,M12,M13],[M21,M22,M23],[M31,M32,M33]]
    # plaintext is the plaintext string of arbitrary length
    # from {a,b,...,z}
    
    # perform the encryption of given plaintext using the given matrix M
    # according to the Hill cipher. Pad the plaintext with 'x' characters to 
    # make its length a multiple of 3.     
    
    # Some helpful funcitons:
    # len(plaintext) : gives the length of the plaintext string
    # one way of selecting chunks of 3 elements from a list:
    # 
    
    # c will be the resulting ciphertext
    #c = ...
    
    matrixinvmod26(M)
    dic={}
    k=0
    for i in range(97,123):
        dic[chr(i)]=k
        k+=1
    
    plaintext=plaintext.lower()
    
    space_indicies=[]
    for i in range(0,len(plaintext)):
        if plaintext[i] == ' ':
            space_indicies.append(i)
        
    char_list=list(plaintext.replace(" ",""))
    
    p_matrix=[]
   
    p_int_matrix=[]
    for i in range(0,len(char_list),len(M)):
        sublist = char_list[i:i+len(M)]  # it means elements i,i+1,i+2 (the last element -1)
        if len(sublist) < len(M):
            diff=len(M) - len(sublist)
            for j in range(0,diff):
                sublist.append('x')
        temp=[]
        for k in sublist:
            temp.append(dic[k])
        p_int_matrix.append(temp)
        
        p_matrix.append(sublist)
        
    
    M=np.array(M)
    p_int_matrix=np.array(p_int_matrix)
    
    c_int_matrix=[]
    
    for i in p_int_matrix:
        c_int_matrix.append(np.matmul(M,i)%26)

    
    c_matrix=[]
    for i in c_int_matrix:
        temp1=[]
        for j in i:
            char_cipher=list(dic.keys())[list(dic.values()).index(j)]
            temp1.append(char_cipher)
        c_matrix.append(temp1)
        
    c=""
    for i in c_matrix:
        c_mid=''.join(i)
        c+=c_mid
        
    for i in space_indicies:
        c=c[:i]+' '+c[i:]
    
    return c


# 3- write the Hill decryption function
def hill_dec(M, ciphertext):
    import numpy as np
    # M is the encryption matrix - Let's assume it's always 3x3 for now
    # M is in the list of lists format i.e.,
    # [[M11,M12,M13],[M21,M22,M23],[M31,M32,M33]]
    # ciphertext is the ciphertext string of arbitrary length
    # from {a,b,...,z}
    
    # perform the decryption of given ciphertext using the given matrix M
    # according to the Hill cipher. 
    
    # p will be the resulting plaintext
    # p = ...
    
    
    M_inv=matrixinvmod26(M)
    dic={}
    k=0
    for i in range(97,123):
        dic[chr(i)]=k
        k+=1
    
    ciphertext=ciphertext.lower()
    
    space_indicies=[]
    for i in range(0,len(ciphertext)):
        if ciphertext[i] == ' ':
            space_indicies.append(i)
            
    char_list=list(ciphertext.replace(" ",""))
    
    c_matrix=[]
   
    c_int_matrix=[]
    for i in range(0,len(char_list),len(M_inv)):
        sublist = char_list[i:i+len(M_inv)]  # it means elements i,i+1,i+2 (the last element -1)
        temp=[]
        for k in sublist:
            temp.append(dic[k])
        c_int_matrix.append(temp)
        
        c_matrix.append(sublist)
        
    
    M_inv=np.array(M_inv)
    c_int_matrix=np.array(c_int_matrix)
    
    p_int_matrix=[]
    
    for i in c_int_matrix:
        p_int_matrix.append(np.matmul(M_inv,i)%26)

    
    p_matrix=[]
    for i in p_int_matrix:
        temp1=[]
        for j in i:
            char_plaintext=list(dic.keys())[list(dic.values()).index(j)]
            temp1.append(char_plaintext)
        p_matrix.append(temp1)
    
    print(p_matrix)
        
    p=""
    for i in p_matrix:
        p_mid=''.join(i)
        p+=p_mid
        
    for i in space_indicies:
        p=p[:i]+' '+p[i:]    

    return p
    



#Usage : print(hill_dec([[17,17,5],[21,18,21],[2,2,19]],'jequzt'))


