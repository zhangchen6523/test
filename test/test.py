# -*- coding: utf-8 -*-
import json
def str_to_hex(s):
    return ' '.join([hex(ord(c)).replace('0x', '') for c in s])

def hex_to_str(s):
    return ''.join([chr(i) for i in [int(b, 16) for b in s.split(' ')]])

def str_to_bin(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])

def bin_to_str(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])


aa='20 20 20 40 20 a8 c2 41 20 20 20 c0 96 40 c3 41 21 03 f6 ee b6'
y = bytearray.fromhex(aa)
z = str(y)
# print(z)
# print(hex_to_str(aa).encode())

print()

