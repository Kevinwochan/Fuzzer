#from handler import handler
from io import StringIO
import csv
import csv
from io import StringIO


class CsvHandler():
    buffer = StringIO()
    def __init__(self, sample_input):
        self.buffer.seek(0)
        self.buffer.truncate(0)
        self.format = []
        self.sample_input_parser(sample_input)
        print(self.format)

    def sample_input_parser(self, sample_input_file_path):
        ''' decomposes CSV into a 2-d list '''
        csvfile = open(sample_input_file_path)
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        parsed_sample = csv.reader(csvfile, dialect)
        for row in parsed_sample:
            self.format.append(row)

    def decompose(self):
        ''' recursive call to decompose complex JSON '''
        #TODO: cant handle complex JSON
        return

    def get_sample(self):
        ''' returns the array of flattenned input '''
        return [format]
    
    def format_data(self, mutated_data):
        ''' uses the mutated_data array to construct a input of the same structure as the sample'''
        #assert len(mutated_data) == len(self.format) * len(self.format) TODO:sanity check
        print(self.format)
        self.writer = csv.writer(self.buffer)
        columns = len(self.format[0])
        index = 0
        for row in self.format:
            self.writer.writerow(mutated_data[index:index + columns])
            index += columns
        return self.buffer.getvalue()
            

if __name__ == '__main__':
    handler = CsvHandler('./files/csv1.txt')
    mutated_csv = handler.format_data(['header', 'must', 'stay', 'intact', 'a', 'b', 'c', 'S', 'aa', 'b', 'c', 'S', 'i', 'j', 'k', 'et'])
    print(mutated_csv)