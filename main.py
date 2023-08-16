from src.dbinfo import DBInfo
from src.backend.node import Node
from src.backend.pager import Pager

def test_dbinfo():
    pager = Pager('test.db')
    data = pager.get_page(1)
    dbinfo = DBInfo(data)
    dbinfo._debug()

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

def test_file_end_to_end():
    # create the pagers for both the old and new dbs
    old_db_pager = Pager('test.db')
    new_db_pager = Pager('generated.db')

    # read in the schema page
    schema_page = old_db_pager.get_page(1)
    dbinfo = DBInfo(schema_page)
    schema_node = Node(schema_page, True)

    # read in the page with the test table
    data_page = old_db_pager.get_page(2)
    data_node = Node(data_page)

    # serialize the pages
    new_schema_page = dbinfo.to_bytes() + schema_node.to_bytes(dbinfo)
    new_data_page = data_node.to_bytes(dbinfo)

    # write the pages to the new db
    new_db_pager.write_page(1, new_schema_page)
    new_db_pager.write_page(2, new_data_page)

    print('generated.db written')

if __name__ == '__main__':
    test_file_end_to_end()
