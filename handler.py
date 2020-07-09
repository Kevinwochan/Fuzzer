class handler(__init__):
    def __init__(self, sample_input):
        self.sample_input = sample_input
        self.byte_positions = self.sample_input_parser(sample_input)

    def sample_input_parser(self, sample_input):
        return []
    
    def format_input(self):
        ''' stitches together mutated '''
        for i in range(len(byte_positions)):
            overflow_mutator(sample_input[i])


