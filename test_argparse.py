import unittest
import argparse
import sys
import argument_parser
import os


class TestArgParse(unittest.TestCase):
    def test_all_flags(self):
        args = ['-m', 'buba', '-d', 'boba', '-w', 'biba',
                '-cc', 'beba', '-z', '-e', '-t']

        parser = argument_parser.create_parser(args)

        self.assertEqual(parser.method, 'buba')
        self.assertEqual(parser.data, 'boba')
        self.assertEqual(parser.wav, 'biba')
        self.assertEqual(parser.cipher_code, 'beba')
        self.assertTrue(parser.zip)
        self.assertTrue(parser.encrypt)
        self.assertTrue(parser.testing)

    def test_failing_encode(self):
        args = ['-m', 'encode_lsb', '-d', 'buba', '-w', 'boba', '-t']
        is_failed = False
        parser = argument_parser.create_parser(args)

        try:
            argument_parser.parse_args(parser)

        except(FileNotFoundError):
            is_failed = True

        finally:
            self.assertTrue(is_failed)

    def test_failing_decode(self):
        args = ['-m', 'decode_lsb', '-w', 'boba', '-t']
        is_failed = False
        parser = argument_parser.create_parser(args)

        try:
            argument_parser.parse_args(parser)

        except(FileNotFoundError):
            is_failed = True

        finally:
            self.assertTrue(is_failed)

    def test_failing_detect(self):
        args = ['-m', 'detect_lsb', '-w', 'boba', '-t']
        is_failed = False
        parser = argument_parser.create_parser(args)

        try:
            argument_parser.parse_args(parser)

        except(FileNotFoundError):
            is_failed = True

        finally:
            self.assertTrue(is_failed)

    def test_encode(self):
        data_path = os.path.join('testing_data', 'data_test.png')
        wav_path = os.path.join('testing_data', 'wav_test.wav')

        args = ['-m', 'encode_lsb', '-d', data_path, '-w', wav_path, '-t']
        is_failed = False
        parser = argument_parser.create_parser(args)

        try:
            argument_parser.parse_args(parser)

        except(FileNotFoundError):
            is_failed = True

        finally:
            self.assertFalse(is_failed)

    def test_decode(self):
        wav_path = os.path.join('testing_data', 'wav_test.wav')

        args = ['-m', 'decode_lsb', '-w', wav_path, '-t']
        is_failed = False
        parser = argument_parser.create_parser(args)

        try:
            argument_parser.parse_args(parser)

        except(FileNotFoundError):
            is_failed = True

        finally:
            self.assertFalse(is_failed)

    def test_detect(self):
        wav_path = os.path.join('testing_data', 'wav_test.wav')

        args = ['-m', 'detect_lsb', '-w', wav_path, '-t']
        is_failed = False
        parser = argument_parser.create_parser(args)

        try:
            argument_parser.parse_args(parser)

        except(FileNotFoundError):
            is_failed = True

        finally:
            self.assertFalse(is_failed)
