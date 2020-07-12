from handler import handler
import json

class JsonHandler(handler):
    def __init__(self, sample_input):
        self.input_data = []
        self.format = dict() 
        self.sample_input_parser(sample_input)

    def sample_input_parser(self, sample_input):
        ''' decomposes JSON into 1.the data, 2.the structure '''
        pos = 0
        parsed_sample = json.loads(sample_input)
        if isinstance(parsed_sample, list): 
            for item in parsed_sample: 
                self.input_data.append(item)
                self.format[pos] = pos+1
                pos+=1
        elif isinstance(parsed_sample, dict): 
            for key, val in parsed_sample.items():
                self.input_data.append(key)
                self.input_data.append(val)
                self.format[pos] = pos+1
                pos+=1
                pos+=1
        else:
            Exception('JSON data type not recognised')

    def decompose(self):
        ''' recursive call to decompose complex JSON '''
        return

    def get_sample(self):
        ''' returns the array of flattenned input '''
        return self.input_data
    
    def format_data(self, mutated_data):
        ''' uses the mutated_data array to construct a input of the same structure as the sample'''
        assert len(mutated_data) == len(self.input_data)
        mutated_input = dict()
        for key, val in self.format.items(): 
            if isinstance(val, list):
               mutated_input[mutated_data.pop(0)] = [mutated_data.pop(0) for i in range(len(val))]
            else:
                key = mutated_data.pop(0)
                value = mutated_data.pop(0)
                mutated_input[key] = value
        return json.dumps(mutated_input)

# TODO: move tests somewhere else?
def test_input_parser_basic():
    '''checks that a json is correctly flattenned'''
    json_string = ''
    with open('./files/json2.txt') as f:
        json_string = ''.join(f.readlines())
    handler = JsonHandler(json_string)
    flattened_json = handler.get_sample()
    assert flattened_json == ["0", 0, "1", 1, "2", 2, "3", 3, "4", 4, "5", 5, "6", 6, "7", 7]

def test_format_data_basic():
    '''checks that a json flattenned and reformed with the same data is the same (associative)'''
    json_string = ''
    with open('./files/json2.txt') as f:
        json_string = ''.join(f.readlines())
    handler = JsonHandler(json_string)
    data = ["0", 0, "1", 1, "2", 2, "3", 3, "4", 4, "5", 5, "6", 6, "7", 7]
    assert handler.format_data(data) == '{"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7}'
