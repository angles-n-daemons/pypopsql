from pager import Pager
from node import Node

def test_btree():
    pager = Pager('test.db')
    data = pager.get_page(2)
    node = Node(data)
    node._debug_print_header()

if __name__ == '__main__':
    test_btree()
