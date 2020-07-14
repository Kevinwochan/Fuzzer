from Handler import Handler
import csv
from io import StringIO


class CsvHandler(Handler):
    buffer = StringIO()
    def __init__(self, sample_input_file_path):
        self.buffer.seek(0)
        self.buffer.truncate(0)
        self.sample = self.parse(sample_input_file_path)

    def data(self):
        return self.sample

    def parse(self, sample_input_file_path):
        ''' decomposes CSV into a 2-d list '''
        rows = []
        csvfile = open(sample_input_file_path)
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        parsed_sample = csv.reader(csvfile, dialect)
        for row in parsed_sample:
            rows.append(row)
        return rows

    def decompose(self):
        ''' recursive call to decompose complex JSON '''
        return

    def format(self, mutated_data):
        ''' uses the mutated_data array to construct a input of the same structure as the sample'''
        #assert len(mutated_data) == len(self.format) * len(self.format) TODO:sanity check
        self.writer = csv.writer(self.buffer)
        columns = len(self.sample[0])
        index = 0
        empty_lines = 0
        for row in self.sample:
            if len(row) == 0:
                empty_lines+=1
            self.writer.writerow(mutated_data[index:index + columns])
            index += columns
        return self.buffer.getvalue() + '\n'*empty_lines
            
