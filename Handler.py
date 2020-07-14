from abc import ABC, abstractmethod

class Handler(ABC):
    @abstractmethod
    def __init__(self, sample_input_file_path):
        '''
        :param sample_input_file_path: the str provided in the binary's txt file, we use a file path since the CSV implementation needs to open the file
        :type sample_input_file_path: str
        '''
        pass

    @property
    @abstractmethod
    def data(self):
        '''
        :return list of fundamanetal data types (float, str, int etc)  to be mutated.
        This will never return a complexe data structure like a list or a dictionary
        :rtype list
        '''
        pass

    @abstractmethod
    def parse(self, sample_input_file_path):
        '''
        Parses the string into a python data structure, storing the layout and data of the sample input

        :param sample_input_file_path: the str provided in the binary's txt file
        :type sample_input_file_path: str
        '''
        pass

    @abstractmethod
    def format(self, mutated_data):
        '''
        Stitches together the format

        :param mutated_data: The data to be formatted into a string
        :type mutated_data: list

        :return a string containing the mutated data, formatted like the sample_input
        :rtype string
        '''
        return ''


