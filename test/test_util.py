import unittest
from unittest import TestCase
from dataclasses import dataclass
from src.util import varint, to_varint


@dataclass
class VarIntTestCase:
    data: bytes
    expected: int
    cursor: int


class TestVarint(TestCase):
    def test_varint(self):
        tests = [
            VarIntTestCase([0x00], 0x00000000, 1),
            VarIntTestCase([0x7f], 0x0000007f, 1),
            VarIntTestCase([0x81, 0x00], 0x00000080, 2),
            VarIntTestCase([0x82, 0x00], 0x00000100, 2),
            VarIntTestCase([0x81, 0x91, 0xd1, 0xac, 0x78], 0x12345678, 5),
            VarIntTestCase([0x81, 0x81, 0x81, 0x81, 0x01], 0x10204081, 5),
        ]

        for test in tests:
            with self.subTest(msg=f'testing varint {test.data} = {test.expected}'):
                input_data = bytes(test.data)
                result, cursor = varint(input_data, 0)
                self.assertEqual(test.expected, result)
                self.assertEqual(test.cursor, cursor)
                self.assertEqual(input_data.hex(), to_varint(result).hex())

    def test_varint_mid_sequence(self):
        result, cursor = varint(bytes([
            0x32, 0x81, 0x7f, 0x91,
        ]), 1)
        self.assertEqual(result, 0x000000ff)
        self.assertEqual(cursor, 3)
        self.assertEqual(bytes([0x81, 0x7f]), to_varint(result))

    def test_varint_full_9_bytes(self):
        input_data = bytes([0x81, 0x81, 0x81, 0x81, 0x81, 0x81, 0x81, 0x81, 0x81])
        result, cursor = varint(input_data, 0)
        self.assertEqual(result, 145249953336295809)
        self.assertEqual(cursor, 9)
        self.assertEqual(input_data, to_varint(result))

if __name__ == '__main__':
    unittest.main()
