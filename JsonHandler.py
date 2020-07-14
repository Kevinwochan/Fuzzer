from Handler import Handler
import json

class JsonHandler(Handler):
    def __init__(self, sample_input_file_path):
        self._data = []
        self.sample = self.parse(sample_input_file_path)

    @property
    def data(self):
        return self._data

    def parse(self, sample_input_file_path):
        '''
            decomposes JSON into an simple array of data
            parsed_sample = {"0": 1, "2": 3}
            self.sample = {
                "0": 1,
                "2": 3
            }
            self._data = ["0", 1, "2", 3]
        '''
        sample_input = ''
        with open(sample_input_file_path) as f:
            sample_input = f.read().replace('\n', '')
        parsed_json = json.loads(sample_input)
        self.decompose(parsed_json)
        return parsed_json

    def decompose(self, data):
        ''' recursive call to decompose complex JSON '''
        if isinstance(data, list): 
            for item in data: 
                self.decompose(item)
        elif isinstance(data, dict): 
            for key, val in data.items():
                self._data.append(key)
                self.decompose(val)
        elif isinstance(data, (str, int, float, bool)):
            self._data.append(data)
        else:
            raise TypeError('JSON data type not recognised')

    def construct(self, structure, mutated_data):
        print()
        print('muated is :' +str(mutated_data))
        print('structure is:' + str(structure))
        if isinstance(structure, list): 
            return [self.construct(item, mutated_data) for item in structure]
        elif isinstance(structure, dict): 
            c = dict()
            for key, val in structure.items():
                key = mutated_data.pop(0)
                val = self.construct(val, mutated_data)
                c[key] = val
            return c
        elif isinstance(structure, (str, int, float, bool)):
            return mutated_data.pop(0)
        else:
            raise TypeError('JSON data type not recognised')
            return None

    def format(self, mutated_data):
        ''' uses the mutated_data array to construct a input of the same structure as the sample'''
        mutated_input = self.construct(self.sample, mutated_data)
        return json.dumps(mutated_input)

