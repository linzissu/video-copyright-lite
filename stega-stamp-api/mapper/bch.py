from flask import Flask, request
import bchlib

BCH_BITS, BCH_POLYNOMIAL = 5, 137
bch = bchlib.BCH(BCH_POLYNOMIAL, BCH_BITS)

def bch_encode(secret):
    if len(secret) > 7:
        print('Error: Can only encode 56bits (7 characters) with ECC')
        return None
    else:
        data = bytearray(secret + ' ' * (7 - len(secret)), 'utf-8')
        ecc = bch.encode(data)
        packet = data + ecc

        packet_binary = ''.join(format(x, '08b') for x in packet)
        secret = [int(x) for x in packet_binary]
        secret.extend([0, 0, 0, 0])
        print(secret)
        return secret

def bch_decode(code):
    packet_binary = "".join([str(int(bit)) for bit in code[:96]])
    packet = bytes(int(packet_binary[i : i + 8], 2) for i in range(0, len(packet_binary), 8))
    packet = bytearray(packet)

    data, ecc = packet[:-bch.ecc_bytes], packet[-bch.ecc_bytes:]

    bitflips = bch.decode_inplace(data, ecc)
    if bitflips != -1:
        secret = data.decode("utf-8")
        print('decode sucess! secret:', secret)
        return secret
    else:
        print('Failed to decode')
        return None
 
