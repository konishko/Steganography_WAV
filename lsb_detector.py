#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import fabs
import wav_parser as wp


def read_bytes_from_file(file_name):
    with open(file_name, 'rb') as file:
        return file.read()


def flip(val):
    if val & 1:
        return val - 1
    return val + 1


def invert_flip(val):
    if val == 0 or val == 255:
        return val
    if val & 1:
        return val + 1
    return val - 1


def discriminant(group):
    group_size = len(group)
    result = 0

    for i in range(group_size - 1):
        result += fabs(group[i + 1] - group[i])

    return result


class LSBDetector():
    def __init__(self, wav_bytes):
        self.wav_bytes = wav_bytes
        self.group_size = 4
        self.flip_mask = [1, 0, 0, 1]
        self.groups = []

    def detect_lsb_rs(self):
        self.header_length = wp.get_header_length(self.wav_bytes)
        self.bytes_per_sample = wp.get_bytes_per_sample(self.wav_bytes)

        pointer = self.header_length
        regular_flip = 0
        regular_inv_flip = 0
        singular_flip = 0
        singular_inv_flip = 0

        while(True):
            if(pointer + self.group_size
               * self.bytes_per_sample < len(self.wav_bytes)):
                self.groups.append(self.wav_bytes[pointer:
                                                  pointer + self.group_size
                                                  * self.bytes_per_sample:
                                                  self.bytes_per_sample])
                pointer += self.group_size * self.bytes_per_sample

            else:
                break

        for group in self.groups:
            initial = discriminant(group)
            flipped_group = []
            inv_flip_group = []

            for i in range(self.group_size):
                if self.flip_mask[i]:
                    flipped_group.append(flip(group[i]))
                    inv_flip_group.append(invert_flip(group[i]))

                else:
                    flipped_group.append(group[i])
                    inv_flip_group.append(group[i])

            flipped = discriminant(flipped_group)
            invert_flipped = discriminant(inv_flip_group)

            if flipped > initial:
                regular_flip += 1
            elif flipped < initial:
                singular_flip += 1

            if invert_flipped > initial:
                regular_inv_flip += 1
            elif invert_flipped < initial:
                singular_inv_flip += 1

        print(regular_flip, singular_flip, regular_inv_flip, singular_inv_flip)

        if(regular_flip * 0.999
           < singular_flip < regular_flip * 1.001
           and regular_inv_flip * 0.999
           < singular_inv_flip < regular_inv_flip * 1.001):
            self.is_suspicious = False
            print('Very low chance of steganography there!')
        else:
            self.is_suspicious = True
            print('Seems here is steganography, try to decode it.')
