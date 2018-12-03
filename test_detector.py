import unittest
import lsb_detector as lsbd
import os
import operations_with_os as owo


class TestLSBDetector(unittest.TestCase):
    def test_suspicious_file(self):
        wav_path = os.path.join('testing_data', 'suspicious_wav.wav')
        wav_bytes = owo.read_bytes_from_file(wav_path)
        detector = lsbd.LSBDetector(wav_bytes)
        detector.detect_lsb_rs()
        self.assertTrue(detector.is_suspicious)

    def test_normal_file(self):
        wav_path = os.path.join('testing_data', 'wav_test.wav')
        wav_bytes = owo.read_bytes_from_file(wav_path)
        detector = lsbd.LSBDetector(wav_bytes)
        detector.detect_lsb_rs()
        self.assertFalse(detector.is_suspicious)
