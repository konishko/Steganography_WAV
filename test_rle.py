import unittest
import rle_modified as rle


class TestRLE(unittest.TestCase):
    def test_encoding(self):
        data = bytes([43, 43, 43, 43, 43, 43, 44, 89, 108, 47, 247])
        expected_result = bytes([134, 43, 5, 44, 89, 108, 47, 247])
        encoder = rle.RLEEncoder(data)
        encoder.encode_rle()
        self.assertEqual(encoder.result, expected_result)

    def test_decoding(self):
        data = bytes([7, 65, 89, 30, 15, 206, 1, 34, 140, 8])
        expected_result = bytes([65, 89, 30, 15, 206, 1, 34,
                                 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8])
        decoder = rle.RLEDecoder(data)
        decoder.decode_rle()
        self.assertEqual(decoder.result, expected_result)
