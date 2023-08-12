from typing import Tuple

def b2i(b: bytes) -> int:
    return int.from_bytes(b, 'big', signed=False)

def varint(b: bytes, cursor: int) -> Tuple[int, int]:
    """
    varint reads a variable length int from a byte string

    it takes the following parameters
     - b: sequence of bytes, generally a full table page
     - cursor: starting index of the varint

    and returns a tuple containing
    - the value of the integer
    - index of the cursor after the last byte of the varint
    """

    result = 0

    for j in range(8):
        i = cursor + j

        # read the next byte into an integer
        byte_num = b[i]

        # result shifts left 7 bits, then the first 7 bits of byte_num are appended
        result = (result << 7) | (byte_num & 0x7f)

        # check the first bit of byte_num to see if we should continue reading
        continue_reading = byte_num & 0x80

        if not continue_reading:
            return result, cursor + j + 1

    # read last byte, use all 8 bytes to fill the remaining spaces
    byte_num = b[cursor + 8]
    result = (result << 8) | byte_num

    return result, cursor + 9

def to_varint(x: int) -> bytes:
    """
    to_varint takes an integer and turns it into a variable length byte array

    it takes x, an integer

    and returns a varint representation as a byte array
    """
    result = bytearray()

    first_7_bits = 0xfe00000000000000
    requires_9_bytes = x & first_7_bits

    # if any of the first 7 bits are filled, 9 bytes will be needed
    first_shift_size = 8 if requires_9_bytes else 7
    first_modulo = 256 if requires_9_bytes else 128

    result.append(x % first_modulo)
    x = x >> first_shift_size

    while x > 0:
        # pull first 7 bits, flip the first bit to signal carryover
        byte = (x % 128) | 0x80
        result.insert(0, byte)
        x = x >> 7

    return bytes(result)
