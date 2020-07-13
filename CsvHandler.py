from handler import handler
import csv

class CsvHandler(handler):
    def __init__(self, sample_input):
        self.input_data = [] # contains flattened data
        self.format = []
        self.sample_input_parse_dialect(sample_input)
        print(input_data)
        self.sample_input_parser(sample_input)
        print(input_data)

    def sample_input_parser(self, sample_input_file_path):
        ''' decomposes JSON into 1.the data, 2.the structure '''
        parsed_sample = csv.DictReader(sample_input_file_path)
        counter = 0
        for row in parsed_sample:
            self.input_data.append(row.values())
            self.format.append([0]*row_values)
        self.input_data.insert(0, rows.keys()) 

    def sample_input_parser_dialect(self, sample_input_file_path):
        csvfile = open(sample_input_file_path)
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        parsed_sample = csv.reader(csvfile, dialect)
        #if (csv.Sniffer().has_header()):


    def decompose(self):
        ''' recursive call to decompose complex JSON '''
        #TODO: cant handle complex JSON
        return

    def get_sample(self):
        ''' returns the array of flattenned input '''
        return self.input_data
    
    def format_data(self, mutated_data):
        ''' uses the mutated_data array to construct a input of the same structure as the sample'''
        len_columns = len(format[0])
        for row in input_data:

if __name__ == '__main__':
    handler = CsvHandler('./files/csv1.txt')