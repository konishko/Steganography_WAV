#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_bytes_per_sample(wav_bytes):
    raw_bytes = wav_bytes[34:36]
    bytes_per_sample = int.from_bytes(raw_bytes,
                                      byteorder='little') // 8

    return bytes_per_sample


def get_header_length(wav_bytes):
    pointer = 0
    length = len(wav_bytes)
    result = None

    while pointer < length - 4:
        if wav_bytes[pointer:pointer + 4] == b'data':
            result = pointer + 8
            break

        else:
            pointer += 1

    if result is None:
        print('Something wrong with your WAV file')
    else:
        return result


def is_bytes_wav(my_bytes):
    return my_bytes[8:12] == b'WAVE'
