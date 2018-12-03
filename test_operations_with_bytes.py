import unittest
import os
import operations_with_bytes_and_bits as owb
import operations_with_os as owo


class TestOperationsWithBytes(unittest.TestCase):
    def test_text_to_bits(self):
        text = 'Nadel мужик shl`yapu, а 0на ему ...'
        result = owb.text_to_bits_string(text)
        expected_result = ('0100111001100001011001000110010101101'
                           + '10000100000110100001011110011010001'
                           + '10000011110100001011011011010000101'
                           + '11000110100001011101000100000011100'
                           + '11011010000110110001100000011110010'
                           + '11000010111000001110101001011000010'
                           + '00001101000010110000001000000011000'
                           + '01101000010111101110100001011000000'
                           + '10000011010000101101011101000010111'
                           + '10011010001100000110010000000101110'
                           + '0010111000101110')
        self.assertEqual(result, expected_result)

    def test_bits_to_text(self):
        bits = ('0100111001100001011001000110010101101'
                + '10000100000110100001011110011010001'
                + '10000011110100001011011011010000101'
                + '11000110100001011101000100000011100'
                + '11011010000110110001100000011110010'
                + '11000010111000001110101001011000010'
                + '00001101000010110000001000000011000'
                + '01101000010111101110100001011000000'
                + '10000011010000101101011101000010111'
                + '10011010001100000110010000000101110'
                + '0010111000101110')
        expected_result = 'Nadel мужик shl`yapu, а 0на ему ...'
        result = owb.text_from_bits_string(bits)

        self.assertEqual(result, expected_result)

    def test_byte_to_bits(self):
        result = owb.byte_to_bits(16543, 16)
        expected_result = '0100000010011111'
        self.assertEqual(result, expected_result)

    def test_bits_to_bytes(self):
        result = owb.bits_to_bytes('0100000010011111')
        expected_result = b'@\x9f'
        self.assertEqual(result, expected_result)

    def test_get_check_sum(self):
        data_path = os.path.join('testing_data', 'data_test.png')
        with open(data_path, 'rb') as file:
            data = file.read()
        result = owb.get_check_sum(data)
        expected_result = 190971
        self.assertEqual(result, expected_result)

    def test_getting_free_name(self):
        name = 'requirements.txt'
        name = owo.get_free_name(name)
        self.assertEqual(name, '(1)requirements.txt')
