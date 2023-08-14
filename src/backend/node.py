from enum import Enum
from typing import Tuple, List

from src.backend.cell import TableLeafCell
from src.dbinfo import DBInfo
from src.util import b2i

class NodeType(Enum):
    INDEX_INTERIOR = 2
    TABLE_INTERIOR = 5
    INDEX_LEAF = 10
    TABLE_LEAF = 13

class Node:
    def __init__(
        self,
        data: bytes,
        db_header: bool=False,
    ):

        self.data = data
        self.page_size = len(data)
        
        self.node_type, \
        self.cell_offset, \
        self.num_cells, \
        self.right_pointer, \
        self.first_freeblock, \
        self.num_fragmented_bytes = self.read_header_bytes(data, db_header)

        self.cells = self.read_cells(data, db_header)

    def read_header_bytes(
        self,
        data: bytes,
        db_header: bool=False,
    ) -> Tuple[
        NodeType,
        int, # num cells
        int, # cell_offset
        int, # right_pointer
        int, # first_freeblock
        int, # num_fragmented_bytes
    ]:
        offset = 100 if db_header else 0

        node_type = NodeType(b2i(data[offset + 0: offset + 1]))

        first_freeblock = b2i(data[offset + 1: offset + 3])

        num_cells = b2i(data[offset + 3: offset + 5])

        cell_offset = b2i(data[offset + 5: offset + 7])

        num_fragmented_bytes = data[offset + 7]

        right_pointer = None
        if not self.is_leaf(node_type):
            right_pointer_bytes = data[offset + 8: offset + 12]
            right_pointer = b2i(right_pointer_bytes)

        return (
            node_type,
            cell_offset,
            num_cells,
            right_pointer,
            first_freeblock,
            num_fragmented_bytes,
        )

    def read_cells(
        self,
        data: bytes,
        db_header: bool=False,
    ) -> List[any]:
        page_header_len = 8 if self.is_leaf() else 12
        db_header_len = 100 if db_header else 0

        cells = []

        for i in range(self.num_cells):
            offset = db_header_len + page_header_len + (i * 2)
            p = b2i(data[offset:offset + 2])
            cell = TableLeafCell(data, p)
            cells.append(cell)

        return cells

    def is_leaf(self, node_type: NodeType = None) -> bool:
        node_type = node_type or self.node_type
        return node_type in (NodeType.TABLE_LEAF, NodeType.INDEX_LEAF)

    def to_bytes(self, dbinfo: DBInfo) -> bytes:
        return bytes([])

    def _debug(self):
        print('node type', self.node_type)
        print('first freeblock', self.first_freeblock)
        print('cell content start', self.cell_offset)
        print('num fragmented bytes', self.num_fragmented_bytes)
        print('right pointer', self.right_pointer)
        print('\n')

        for i, cell in enumerate(self.cells):
            cell._debug()
