import pytest
from JsonHandler import JsonHandler

@pytest.fixture
def basic_json():
    return './files/json2.txt'

@pytest.fixture
def json_with_list():
    return './files/json1.txt'
 
def test_input_parser_basic(basic_json):
    '''checks that a json is correctly flattenned'''
    handler = JsonHandler(basic_json)
    flattened_json = handler.data
    assert flattened_json == ["0", 0, "1", 1, "2", 2, "3", 3, "4", 4, "5", 5, "6", 6, "7", 7]

def test_format_data_basic(basic_json):
    '''checks that a json flattenned and reformed with the same data is the same (associative)'''
    handler = JsonHandler(basic_json)
    data = ["0", 0, "1", 1, "2", 2, "3", 3, "4", 4, "5", 5, "6", 6, "7", 7]
    assert handler.format(data) == '{"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7}'

def test_format_data_with_mutation(basic_json):
    '''checks that a json reformed with the new data is the same except with the mutated field'''
    handler = JsonHandler(basic_json)
    data = ["A"*10, 0, "1", 1, "2", 2, "3", 3, "4", 4, "5", 5, "6", 6, "7", 7]
    assert handler.format(data) == '{"' + 'A'*10 +'": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7}'



def test_input_parser_list(json_with_list):
    '''checks that a json is correctly flattenned'''
    handler = JsonHandler(json_with_list)
    flattened_json = handler.data
    assert flattened_json == [ "len", 12, "input", "AAAABBBBCCCC", "more_data", "a", "bb"]

def test_format_data_list(json_with_list):
    '''checks that a json flattenned and reformed with the same data is the same (associative)'''
    handler = JsonHandler(json_with_list)
    data = [ "len", 12, "input", "AAAABBBBCCCC", "more_data", "a", "bb"]
    assert handler.format(data) == '{"len": 12, "input": "AAAABBBBCCCC", "more_data": ["a", "bb"]}'

def test_format_data_mutated_json_list(json_with_list):
    '''checks that a json reformed with the new data is the same except with the mutated field'''
    handler = JsonHandler(json_with_list)
    data = [ "len", 12, "input", "A"*20, "more_data", "a", "bb"]
    assert handler.format(data) == '{"len": 12, "input": "'+'A'*20+'", "more_data": ["a", "bb"]}'

