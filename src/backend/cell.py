from src.backend.record import Record
from src.util import to_varint, varint

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

        self.payload = data[cursor:cursor+self.payload_size]
        self.record = Record(data, cursor)
        self.cursor = cursor + self.payload_size

    def to_bytes(self):
        payload = self.record.to_bytes()
        payload_size_bytes = to_varint(len(payload))
        row_id_bytes = to_varint(self.row_id)
        return payload_size_bytes + row_id_bytes + payload

    def _debug(self):
        print('cell at index', self.pointer)
        print('payload size', self.payload_size)
        print('row id', self.row_id)
        self.record._debug()
        print('\n')
