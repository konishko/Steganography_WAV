from collections import deque


def read_bytes_from_file(file_name):
    with open(file_name, 'rb') as file:
        return file.read()


def byte_to_bits(byte, bits_count):
    return bin(byte)[2:].zfill(bits_count)


class RLEEncoder():
    def __init__(self, data):
        self.result = bytearray()
        self.different_bytes = deque()
        self.same_bytes_count = 0
        self.data = data
        self.previous_byte = None

    def check_different_bytes(self):
        if len(self.different_bytes) > 0:
            while(True):
                length = len(self.different_bytes)
                if length > 127:
                    self.result.append(127)
                    for _ in range(127):
                        self.result.append(self.different_bytes.popleft())

                else:
                    new_byte = '0' + byte_to_bits(len(self.different_bytes), 7)
                    self.result.append(int(new_byte, base=2))
                    for _ in range(length):
                        self.result.append(self.different_bytes.popleft())

                    break

    def check_same_bytes(self):
        if self.same_bytes_count > 0:
            while(True):
                if self.same_bytes_count > 127:
                    self.result.append(255)
                    self.result.append(self.previous_byte)
                    self.same_bytes_count -= 127

                else:
                    new_byte = '1' + byte_to_bits(self.same_bytes_count, 7)
                    self.result.append(int(new_byte, base=2))
                    self.result.append(self.previous_byte)

                    break

    def encode_rle(self):
        for byte in self.data:
            if self.previous_byte is None:
                self.previous_byte = byte
                if self.data[1] != byte:
                    self.different_bytes.append(byte)
                else:
                    self.same_bytes_count += 1

                continue

            if self.previous_byte == byte:
                self.check_different_bytes()

                self.same_bytes_count += 1

            else:
                self.check_same_bytes()

                self.previous_byte = byte
                self.same_bytes_count = 0
                self.different_bytes.append(byte)

        self.check_different_bytes()
        self.check_same_bytes()

        self.result = bytes(self.result)


class RLEDecoder():
    def __init__(self, data):
        self.result = bytearray()
        self.data = data
        self.length = len(self.data)
        self.pointer = 0

    def decode_rle(self):
        while(True):
            if self.pointer >= self.length:
                break

            if self.data[self.pointer] >> 7:
                self.pointer += 1
                for _ in range(self.data[self.pointer - 1] & 127):
                    self.result.append(self.data[self.pointer])

            else:
                for _ in range(self.data[self.pointer] & 127):
                    self.pointer += 1
                    self.result.append(self.data[self.pointer])

            self.pointer += 1

        self.result = bytes(self.result)
