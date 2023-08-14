from unittest import TestCase

from src.backend.cell import TableLeafCell

class TestCell(TestCase):
    def test_table_leaf_cell(self):
        data = bytes([
            0x06, # payload size
            0x02, # row id
            0x03, 0x11, 0x01, 0x79, 0x6f, 0x02, # payload
        ])
        cell = TableLeafCell(data, 0)
        self.assertEquals(cell.payload_size, 6)
        self.assertEquals(cell.row_id, 2)
        self.assertEquals(cell.payload, data[2:])
        self.assertEquals(cell.cursor, 8)
        self.assertEquals(cell.to_bytes(), data)

if __name__ == '__main__':
    unittest.main()
