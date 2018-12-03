#!/usr/bin/env python
# -*- coding: utf-8 -*-


def text_to_bits_string(text, encoding="utf-8"):
    bits = bin(int.from_bytes(text.encode(encoding), byteorder='big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits_string(bits, encoding='utf-8'):
    text = int(bits, base=2)
    return text.to_bytes((text.bit_length() + 7) // 8,
                         byteorder='big').decode(encoding)


def byte_to_bits(byte, bits_count):
    return bin(byte)[2:].zfill(bits_count)


def bits_to_bytes(bit_string):
    result = bytearray()
    binary_byte = ''
    for bit in bit_string:
        if len(binary_byte) < 8:
            binary_byte += bit

        else:
            result.append(int(binary_byte, base=2))
            binary_byte = bit
    result.append(int(binary_byte, base=2))
    return result


def get_check_sum(bytes):
    counter = 0
    check_sum = 0
    for byte in bytes:
        check_sum += byte * counter % 10
        counter += 1

    return check_sum
