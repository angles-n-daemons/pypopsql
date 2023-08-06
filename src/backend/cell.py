from src.backend.record import Record
from src.util import varint

class TableLeafCell:
    def __init__(
        self,
        data: bytes,
        pointer: int,
    ):
        self.pointer = pointer
        cursor = pointer
        self.payload_size, cursor = varint(data, cursor)
        self.row_id, cursor = varint(data, cursor)

        self.payload_data = data[cursor:cursor+self.payload_size]
        self.record = Record(data, cursor)

    def _debug(self):
        print('cell at index', self.pointer)
        print('payload size', self.payload_size)
        print('row id', self.row_id)
        self.record._debug()
        print('\n')
