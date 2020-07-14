import pytest
from CsvHandler import CsvHandler

@pytest.fixture
def basic_csv():
    return './files/csv1.txt'


def test_input_parser_basic(basic_csv):
    '''checks that a csv is correctly flattenned'''
    handler = CsvHandler(basic_csv)
    flattened_csv = handler.sample
    data = ['header', 'must', 'stay', 'intact', 'a', 'b', 'c', 'S', 'aa', 'b', 'c', 'S', 'i', 'j', 'k', 'et','','','']
    assert flattened_csv == handler.format(data)

def test_format_data_basic(basic_csv):
    '''checks that a csv flattenned and reformed with the same data is the same (associative)'''
    handler = CsvHandler(basic_csv)
    data = ['header', 'must', 'stay', 'intact', 'a', 'b', 'c', 'S', 'aa', 'b', 'c', 'S', 'i', 'j', 'k', 'et']
    print(handler.format(data))
    assert handler.format(data) == '{"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7}'

def test_format_data_with_mutation(basic_csv):
    '''checks that a csv reformed with the new data is the same except with the mutated field'''
    handler = CsvHandler(basic_csv)
    data = ['header', 'must', 'stay', 'intact', 'a'*10, 'b', 'c', 'S', 'aa', 'b', 'c', 'S', 'i', 'j', 'k', 'et',[], [], []]
    assert handler.format(data).strip() == '''
    header,must,stay,intact
    AAAAAAAAAA,0,1,1
    2,2,3,3
    4,4,5,5
    6,6,7,7'
    '''.strip()
