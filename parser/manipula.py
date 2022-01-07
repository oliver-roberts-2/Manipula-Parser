'''
File containing the manipula parser class.

'''


from scanner import Scanner
from custom_parser import Parser
from python_printer import PythonPrinter


class Manipula:
    

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.get_file_string()
        self.parse_file()
        self.write_python()
        
        
    def get_file_string(self):
        ''' Function to get the source file and return the file string. '''
        with open(self.path_to_file, 'r') as file:
            self.file_string = file.read()
            file.close()
        

    def parse_file(self):
        ''' Function to parse the read file. '''
        self.scanner = Scanner(self.file_string)
        self.tokens = self.scanner.tokens
        if self.scanner.had_error:
            print('Error(s) exists in syntax, cannot scan file.')
        self.parser = Parser(self.tokens)
        self.statements = self.parser.parse()
        if self.parser.had_error:
            print('Error(s) exists in tokens, cannot parse file.')
        
    
    def write_python(self):
        ''' Function to write the parsed statements into Python syntax. '''
        PythonPrinter._write(self.statements)
    

manip = Manipula('sample_text.txt')


