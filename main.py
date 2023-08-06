from src.dbinfo import DBInfo
from src.backend.node import Node
from src.backend.pager import Pager

def test_btree():
    pager = Pager('test.db')
    data = pager.get_page(2)
    node = Node(data)
    node._debug()

def test_schema_page():
    pager = Pager('test.db')
    data = pager.get_page(1)

    dbinfo = DBInfo(data)
    dbinfo._debug()

    node = Node(data, True)
    node._debug()

if __name__ == '__main__':
    test_schema_page()
