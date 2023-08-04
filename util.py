def b2i(b: bytes):
    return int.from_bytes(b, 'big', signed=False)
