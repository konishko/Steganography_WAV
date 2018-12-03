#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import lsb_detector
import steg_wav
import operations_with_os as owo


def create_parser(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--method', help='Method of WAV process')
    parser.add_argument('-d', '--data', help='File you want to encrypt')
    parser.add_argument('-w', '--wav', help='WAV file you want to process')
    parser.add_argument('-cc', '--cipher_code', help='File with cipher code'
                                                     ' you want to use as a'
                                                     ' key for encrypted'
                                                     ' WAV file')
    parser.add_argument('-z', '--zip', default=False, action='store_true',
                        help='Pack file')
    parser.add_argument('-e', '--encrypt', default=False, action='store_true',
                        help='Encrypt file')
    parser.add_argument('-t', '--testing', default=False, action='store_true',
                        help='Testing mode')

    return parser.parse_args(args)


def parse_args(parser):
    if parser.method == 'encode_lsb':
        wav_bytes = owo.read_bytes_from_file(parser.wav)
        data_bytes = owo.read_bytes_from_file(parser.data)

        if not parser.testing:
            encoder = steg_wav.EncoderLSB(parser.data, data_bytes,
                                          wav_bytes, parser.zip,
                                          parser.encrypt)
            encoder.encode_lsb()

    if parser.method == 'decode_lsb':
        wav_bytes = owo.read_bytes_from_file(parser.wav)
        if parser.cipher_code is not None:
            cipher_code = owo.read_bytes_from_file(parser.cipher_code)
        else:
            cipher_code = None

        if not parser.testing:
            decoder = steg_wav.DecoderLSB(wav_bytes, cipher_code)
            decoder.decode_lsb()

    if parser.method == 'detect_lsb':
        wav_bytes = owo.read_bytes_from_file(parser.wav)

        if not parser.testing:
            detector = lsb_detector.LSBDetector(wav_bytes)
            detector.detect_lsb_rs()
