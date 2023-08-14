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
        self.assertEqual(cell.payload_size, 6)
        self.assertEqual(cell.row_id, 2)
        self.assertEqual(cell.payload, data[2:])
        self.assertEqual(cell.cursor, 8)
        self.assertEqual(cell.to_bytes(), data)

if __name__ == '__main__':
    unittest.main()
