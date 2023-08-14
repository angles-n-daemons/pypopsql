from enum import Enum
from typing import List, Tuple
from dataclasses import dataclass

from src.util import b2i, to_varint, varint

class ColumnType(Enum):
    UNKNOWN = -1
    NULL = 0
    TINYINT = 1
    SMALLINT = 2
    SMALLISHINT = 3
    INTEGER = 4
    BIGGISHINT = 5
    LONG = 6
    IEEE754INT = 7
    ZERO = 8
    ONE = 9
    RESERVED_1 = 10
    RESERVED_2 = 11
    BLOB = 12
    TEXT = 13

    @classmethod
    def _missing_(cls, value: int):
        if value < 12:
            return cls(value)
        elif value % 2 == 0:
            return cls(12)
        else:
            return cls(13)

@dataclass
class Column:
    def __init__(self, column_type: ColumnType, length: int=None):
        self.type = column_type
        self.length = length

    def __repr__(self) -> str:
        return f'column: {self.type}, {self.length}'

    def to_int(self) -> int:
        if self.type.value < 12:
            return self.type.value

        modifier = self.type.value
        return (self.length * 2) + modifier

    def to_bytes(self) -> bytes:
        return to_varint(self.to_int())

    @classmethod
    def from_int(cls, value: int):
        column_type = ColumnType(value)
        length = None

        # calculate length for BLOB and TEXT types as documented
        if column_type == ColumnType.BLOB:
            length = (value - 12) // 2
        elif column_type == ColumnType.TEXT:
            length = (value - 13) // 2

        return cls(column_type, length)

    def to_int(self) -> int:
        if self.type.value < 12:
            return self.type.value
        elif self.type == ColumnType.BLOB:
            return 12 + (self.length * 2)
        elif self.type == ColumnType.TEXT:
            return 13 + (self.length * 2)


class Record:
    def __init__(
        self,
        data: bytes,
        cursor: int,
    ):
        self.data = data

        self.columns, cursor = self.read_column_types(data, cursor)
        self.values, cursor = self.read_values(data, cursor)

        self.cursor = cursor

    def read_column_types(
        self,
        data: bytes,
        cursor: int,
    ) -> Tuple[List[Column], int]:
        columns = []
        cursor_start = cursor
        num_bytes_header, cursor = varint(data, cursor)

        while cursor - cursor_start < num_bytes_header:
            column_type_int, cursor = varint(data, cursor)
            columns.append(Column.from_int(column_type_int))

        return columns, cursor

    def read_values(
        self,
        data: bytes,
        cursor: int,
    ) -> Tuple[List[any], int]:
        values = []
        for column in self.columns:
            value, cursor = self.read_value(column.type, data, cursor, column.length)
            values.append(value)
        return values, cursor

    @staticmethod
    def read_value(
        column_type: ColumnType,
        data: bytes,
        cursor: int,
        length: int = None,
    ) -> Tuple[any, int]:
        if column_type == ColumnType.NULL:
            return None, cursor
        elif column_type == ColumnType.TINYINT:
            return int(data[cursor]), cursor + 1
        elif column_type == ColumnType.SMALLINT:
            return b2i(data[cursor: cursor + 2]), cursor + 2
        elif column_type == ColumnType.SMALLISHINT:
            return b2i(data[cursor: cursor + 3]), cursor + 3
        elif column_type == ColumnType.INTEGER:
            return b2i(data[cursor: cursor + 4]), cursor + 4
        elif column_type == ColumnType.BIGGISHINT:
            return b2i(data[cursor: cursor + 6]), cursor + 6
        elif column_type == ColumnType.LONG:
            return b2i(data[cursor: cursor + 8]), cursor + 8
        elif column_type == ColumnType.ZERO:
            return 0, cursor
        elif column_type == ColumnType.ONE:
            return 1, cursor
        elif column_type == ColumnType.BLOB:
            return data[cursor: cursor + length], cursor + length
        elif column_type == ColumnType.TEXT:
            return data[cursor: cursor + length].decode('utf-8'), cursor + length
        else:
            raise Exception(f'cannot parse column type {column_type}')

    def header_bytes(self) -> bytes:
        payload = bytearray()

        for column in self.columns:
            payload += column.to_bytes()

        payload_size = len(payload)
        if payload_size > 32765:
            raise Exception(f'unexpected header payload size {payload_size}')

        expected_varint_length = 1 if payload_size < 128 else 2
        header_size_bytes = to_varint(payload_size + expected_varint_length)
        return bytes(header_size_bytes + payload)

    @staticmethod
    def value_bytes(column: Column, value: any) -> bytes:
        if column.type == ColumnType.NULL:
            return bytes([])
        elif column.type == ColumnType.TINYINT:
            return value.to_bytes(1)
        elif column.type == ColumnType.SMALLINT:
            return value.to_bytes(2)
        elif column.type == ColumnType.SMALLISHINT:
            return value.to_bytes(3)
        elif column.type == ColumnType.INTEGER:
            return value.to_bytes(4)
        elif column.type == ColumnType.BIGGISHINT:
            return value.to_bytes(6)
        elif column.type == ColumnType.LONG:
            return value.to_bytes(8)
        elif column.type == ColumnType.ZERO:
            return bytes([])
        elif column.type == ColumnType.ONE:
            return bytes([])
        elif column.type == ColumnType.BLOB:
            return value
        elif column.type == ColumnType.TEXT:
            return bytes(value, 'utf-8')
        else:
            raise Exception(f'cannot parse column type {column_type}')

    def values_bytes(self) -> bytes:
        body = bytearray()

        for i, column in enumerate(self.columns):
            body += self.value_bytes(column, self.values[i])

        return bytes(body)

    def to_bytes(self) -> bytes:
        header_bytes = self.header_bytes()
        values_bytes = self.values_bytes()

        return header_bytes + values_bytes

    def _debug(self):
        for i, column in enumerate(self.columns):
            print('column type', column.type)
            print('value', self.values[i])

