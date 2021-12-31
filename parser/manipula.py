'''
File containing the manipula parser class.

'''


from scanner import Scanner
from custom_parser import Parser
from interpreter import Interpreter


class Manipula():
    
    # lexemes are raw substrings of the source code
    # e.g. `language` `=` `'manipula'`
    # tokens are lexems bundled together with other data, tokens are formed
    # e.g. is that lexeme a keyword?
    # Trees:
    # Leaf nodes are numbers, and interior nodes are operators with branches for each of their operands.

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.get_file_string()
        self.interpreter = Interpreter()
        self.parse_file()
        
        
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
        self.interpreter.interpret(self.statements)
    

manip = Manipula('sample_text.txt')          


