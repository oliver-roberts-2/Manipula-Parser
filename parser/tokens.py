'''
File to store the token type and class object.

'''


from enum import Enum

    
class TokenType(Enum):
    ''' 
    Enumerator class to store the token types.
    
    These are the token representations in Python.
    
    '''
    # Single character tokens
    LEFT_PAREN, RIGHT_PAREN = '(', ')'
    LEFT_SQUARE, RIGHT_SQUARE = '[', ']'
    COMMA, DOT = ',', '.'
    MINUS, PLUS = '-', '+'
    SEMICOLON, COLON = ';', ':'
    FWD_SLASH = '/'
    STAR = '*'
    
    # One or two character tokens
    BANG, BANG_EQUAL = '!', '!='
    EQUAL, EQUAL_EQUAL = '=', '=='
    GREATER, GREATER_EQUAL = '>', '>='
    LESS, LESS_EQUAL = '<', '<='
    
    # Literals
    IDENTIFIER = object()
    STRING = str()
    NUMBER = float()
    # For some reason float() caused it to be TokenType.INT
    # In [1]: TokenType.FLOAT
    # Out[1]: <TokenType.INT 0>

    # Keywords
    IF, ELIF, ELSE = 'if', 'elif', 'else'
    AND, OR = 'and', 'or'
    NOT, IN = 'not', 'in'
    TRUE, FALSE = 'True', 'False'
    FOR, WHILE = 'for', 'while'
    
    # End of file
    EOF = None
    
    
class Token():

    
    def __init__(self, token_type, lexeme, literal, line_number):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line_number = line_number
        
        
    def __repr__(self):
        return f'{self.type.name} {self.lexeme} on line {self.line_number}'
    
    
    