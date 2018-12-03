import unittest
import os
import steg_wav as sw
import operations_with_os as owo


class TestEncoderLSB(unittest.TestCase):
    def test_decrypting(self):
        encrypted_data_path = os.path.join('testing_data', 'encrypted_data')
        data_bytes = owo.read_bytes_from_file(encrypted_data_path)
        cipher_code_path = os.path.join('testing_data', 'cipher_key.txt')
        data_path = os.path.join('testing_data', 'data_test.png')
        expected_result = owo.read_bytes_from_file(data_path)
        decoder = sw.DecoderLSB(bytes(), cipher_code_path)
        decoder.testing = True
        decoder.result = data_bytes
        decoder.decrypt()
        self.assertEqual(decoder.result, expected_result)

    def test_simple_decoding(self):
        data_path = os.path.join('testing_data', 'data_test.png')
        expected_data_bytes = owo.read_bytes_from_file(data_path)
        wav_path = os.path.join('testing_data', 'result.wav')
        wav_bytes = owo.read_bytes_from_file(wav_path)
        decoder = sw.DecoderLSB(wav_bytes, None)
        decoder.testing = True
        decoder.decode_lsb()
        result_bytes = decoder.result
        self.assertEqual(result_bytes, expected_data_bytes)
