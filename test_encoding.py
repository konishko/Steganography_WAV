import unittest
import os
import steg_wav as sw
import operations_with_os as owo


class TestEncoderLSB(unittest.TestCase):
    def test_encrypting(self):
        data_path = os.path.join('testing_data', 'data_test.png')
        data_bytes = owo.read_bytes_from_file(data_path)
        encoder = sw.EncoderLSB('data_test', data_bytes, bytes(), 0, 0)
        encoder.testing = True
        encoder.encrypt()
        self.assertNotEqual(encoder.data_bytes, data_bytes)

    def test_getting_bits_string(self):
        data_path = os.path.join('testing_data', 'data_test.png')
        data_bytes = owo.read_bytes_from_file(data_path)
        bits_path = os.path.join('testing_data', 'bits_string_test.txt')
        with open(bits_path, 'r') as file:
            bits_string = file.read()
        encoder = sw.EncoderLSB('data_test.png', data_bytes, bytes(), 0, 0)
        encoder.testing = True
        encoder.get_bits_string()
        self.assertEqual(encoder.binary_info, bits_string)

    def test_simple_encoding(self):
        data_path = os.path.join('testing_data', 'data_test.png')
        data_bytes = owo.read_bytes_from_file(data_path)
        wav_path = os.path.join('testing_data', 'wav_test.wav')
        wav_bytes = owo.read_bytes_from_file(wav_path)
        encoder = sw.EncoderLSB('data_test.png', data_bytes, wav_bytes, 0, 0)
        encoder.testing = True
        encoder.encode_lsb()
        result_bytes = encoder.result
        result_path = os.path.join('testing_data', 'result.wav')
        expected_result_bytes = owo.read_bytes_from_file(result_path)
        self.assertEqual(result_bytes, expected_result_bytes)
