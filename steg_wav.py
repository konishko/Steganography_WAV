#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argument_parser
import time
import operations_with_bytes_and_bits as owbb
import operations_with_os as owo
import rle_modified
import wav_parser as wp
from cryptography.fernet import Fernet


class EncoderLSB():
    def __init__(self, data_name, data_bytes, wav_bytes, zip, encrypt):
        self.wav_bytes = wav_bytes
        self.data_bytes = data_bytes
        self.to_zip = zip
        self.to_encrypt = encrypt
        self.check_sum = owbb.get_check_sum(self.data_bytes)
        self.name = os.path.basename(data_name)
        self.pointer = 0
        self.result = bytearray()
        self.testing = False
        self.bytes_for_data_length = 32
        self.bytes_for_check_sum_length = 32
        self.bytes_for_name_length = 16

    def encode_lsb(self):
        if wp.is_bytes_wav(self.wav_bytes):
            self.bytes_per_sample = wp.get_bytes_per_sample(self.wav_bytes)
            self.header_length = wp.get_header_length(self.wav_bytes)
            self.get_bits_string()
            self.binary_info_length = len(self.binary_info)
            if len(self.wav_bytes) > self.binary_info_length:
                self.get_result_bytes()
                save_time = time.time()
                self.result_name = ('output_steg_lsb{}.wav'
                                    .format(save_time))
                if not self.testing:
                    owo.write_bytes_to_file(self.result,
                                            self.result_name)
                    if self.to_encrypt:
                        owo.write_bytes_to_file(self.cipher_key,
                                                'cipher_key{}.txt'
                                                .format(save_time))
            else:
                print('Gived information is too big for given WAV file')
        else:
            print('You need WAV file for stego')

    def get_bits_string(self):
        binary_name = owbb.text_to_bits_string(self.name)
        name_length = len(binary_name)
        binary_name_length = owbb.byte_to_bits(name_length,
                                               self.bytes_for_name_length)
        binary_check_sum = owbb.byte_to_bits(self.check_sum,
                                             self.bytes_for_check_sum_length)
        if self.to_zip:
            self.pack()

        if self.to_encrypt:
            self.encrypt()

        binary_data = ''
        for byte in self.data_bytes:
            binary_data += owbb.byte_to_bits(byte, 8)
        data_length = len(binary_data)
        binary_data_length = owbb.byte_to_bits(data_length,
                                               self.bytes_for_data_length)
        self.binary_info = (str(int(self.to_zip))
                            + str(int(self.to_encrypt))
                            + binary_data_length
                            + binary_name_length
                            + binary_name
                            + binary_check_sum
                            + binary_data)

    def get_result_bytes(self):
        simple_pointer = 0
        for byte in self.wav_bytes:
            if (self.header_length <= self.pointer < (self.header_length
                                                      + self.binary_info_length
                                                      * self.bytes_per_sample)
               and ((self.pointer - self.header_length)
                    % self.bytes_per_sample == 0)):
                byte = ((byte & 254) | int(self.binary_info[simple_pointer]))
                simple_pointer += 1

            self.result.append(byte)
            self.pointer += 1

    def encrypt(self):
        self.cipher_key = Fernet.generate_key()
        cipher = Fernet(self.cipher_key)
        self.data_bytes = cipher.encrypt(self.data_bytes)

    def pack(self):
        packer = rle_modified.RLEEncoder(self.data_bytes)
        packer.encode_rle()
        if len(packer.result) < len(self.data_bytes):
            self.data_bytes = packer.result


class DecoderLSB():
    def __init__(self, wav_bytes, cipher_code):
        self.wav_bytes = wav_bytes
        self.cipher_code = cipher_code
        self.bytes_for_length = 32
        self.bytes_for_check_sum_length = 32
        self.bytes_for_name_length = 16
        self.name_length = 0
        self.info_length = 0
        self.testing = False
        self.binary_result = ''
        self.name = ''
        self.check_sum = ''
        self.byted_info_length = ''
        self.byted_name_length = ''
        self.byted_check_sum_length = ''

    def decode_lsb(self):
        if wp.is_bytes_wav(self.wav_bytes):
            self.bytes_per_sample = wp.get_bytes_per_sample(self.wav_bytes)
            self.header_length = wp.get_header_length(self.wav_bytes)
            self.get_result_bytes_and_name()
            self.name = owo.get_free_name(self.name)
            print('Initial checksum : {}'.format(self.check_sum))
            print('Checksum of recieved file : {}'
                  .format(owbb.get_check_sum(self.result)))
            if not self.testing:
                owo.write_bytes_to_file(self.result, self.name)
        else:
            print('Gived file is not WAV')

    def get_result_bytes_and_name(self):
        start_of_section = self.header_length
        end_of_section = start_of_section + self.bytes_per_sample
        zip_bit = self.wav_bytes[self.header_length] & 1
        encrypt_bit = self.wav_bytes[self.header_length
                                     + self.bytes_per_sample] & 1

        decomposition_dict = {'info length': [0, self.byted_info_length],
                              'name length': [(self.bytes_for_name_length
                                               * self.bytes_per_sample),
                                              self.byted_name_length],
                              'name': [self.name_length, self.name],
                              'checksum': [(self.bytes_for_check_sum_length
                                            * self.bytes_per_sample),
                                           self.check_sum],
                              'info': [self.info_length, self.binary_result]}

        if int(encrypt_bit) and self.cipher_code is None:
            raise AttributeError('You need cipher code to decrypt that file')

        for key in decomposition_dict.keys():
            pair = decomposition_dict[key]
            if key == 'info length':
                start_of_section = (end_of_section
                                    + self.bytes_per_sample)
                end_of_section = (start_of_section
                                  + (self.bytes_for_length
                                     * self.bytes_per_sample))
            else:
                start_of_section = end_of_section
                end_of_section += pair[0]

            print('Working at {}...'.format(key))
            for byte in self.wav_bytes[start_of_section:
                                       end_of_section:
                                       self.bytes_per_sample]:
                pair[1] += (str)(byte & 1)

            if key == 'info length':
                self.info_length = int(pair[1], base=2) * self.bytes_per_sample
                decomposition_dict['info'][0] = self.info_length
                print(self.info_length)

            if key == 'name length':
                self.name_length = int(pair[1], base=2) * self.bytes_per_sample
                decomposition_dict['name'][0] = self.name_length
                print(self.name_length)

            if key == 'name':
                self.name = owbb.text_from_bits_string(pair[1])
                print(self.name)

            if key == 'checksum':
                self.check_sum = int(pair[1], base=2)

            if key == 'info':
                self.result = owbb.bits_to_bytes(pair[1])
                if int(encrypt_bit):
                    self.decrypt()
                if int(zip_bit):
                    self.unpack()

    def decrypt(self):
        cipher_key = owo.read_bytes_from_file(self.cipher_code)
        cipher = Fernet(cipher_key)
        self.result = cipher.decrypt(bytes(self.result))

    def unpack(self):
        unpacker = rle_modified.RLEDecoder(self.result)
        unpacker.decode_rle()
        self.result = unpacker.result


if __name__ == '__main__':
    parsed_args = argument_parser.create_parser(sys.argv[1:])
    argument_parser.parse_args(parsed_args)
