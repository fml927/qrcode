# -*- coding: utf-8 -*-

from mylibs.constant import *
        
#ecc: Error Correction Codewords
def encode(ver, ecl, data_codewords):
    en = ecc_num_per_block[ver-1][lindex[ecl]]
    ecc = []
    for dc in data_codewords:
        ecc.append(get_ecc(dc, en))
    return ecc

def get_ecc(dc, ecc_num):
    gp = GP_list[ecc_num]
    remainder = dc
    for i in range(len(dc)):
        remainder = divide(remainder, *gp)
    return remainder
    
def divide(MP, *GP):
    po2 = get_power_of_2_list()
    log = get_log_list(po2)
    GP = list(GP)
    for i in range(len(GP)):
        GP[i] += log[MP[0]]
        if GP[i] > 255:
            GP[i] %= 255
        GP[i] = po2[GP[i]]
    
    return XOR(MP, GP)
    
    
def XOR(MP, GP):
    a = len(MP) - len(GP)
    if a < 0:
        MP += [0] * (-a)
    elif a > 0:
        GP += [0] * a
    
    remainder = []
    for i in range(len(MP)):
        remainder.append(MP[i]^GP[i])
    remainder = [i for i in remainder if i]
    return remainder
    
def get_power_of_2_list():
    po2 = [1]
    for i in range(255):
        a = po2[i] * 2
        if a > 255:
            a ^= 285
        po2.append(a)
    return po2
    
def get_log_list(po2):
    log = [None]*256
    for i in range(255):
        log[po2[i]] = i
    return log