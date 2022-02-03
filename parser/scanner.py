'''
File containing the scanner class.

'''


from tokens import TokenType, Token


class Scanner():


    def __init__(self, source):
        self.source = source
        self.had_error = False
        self.errors = []
        self.tokens = []
        self.current = 0
        self.line_number = 1
        self.braces_counter = 0
        
        # Dictionary of Manipula keywords
        self.keywords = {
            'IF': TokenType.IF,
            'ELSEIF': TokenType.ELIF,
            'ELSE': TokenType.ELSE,
            'AND': TokenType.AND,
            'OR': TokenType.OR,
            'FOR': TokenType.FOR,
            'IN': TokenType.IN,
            'TO': TokenType.TO,
            'THEN': TokenType.THEN,
            'DO': TokenType.DO,
            'ENDIF': TokenType.ENDIF,
            'ENDDO': TokenType.ENDDO,
            'TRUE': TokenType.TRUE,
            'FALSE': TokenType.FALSE,
            'WHILE': TokenType.WHILE,
            'PRINT': TokenType.PRINT,
            'VAR': TokenType.VAR,
            'NOT': TokenType.NOT,
            'NULL': None
            }
        
        self.scan_source_code() 
        
    
    def error(self, message):
        ''' Function to create an error and store in errors list. '''
        self.had_error = True
        error_message = f'{message} on line {self.line_number}.'
        self.errors.append(error_message)
        print(error_message)


    def at_end(self):
        ''' Function to check if at end of source code. '''
        return self.current >= len(self.source)
            
    
    def advance(self):
        ''' Function to advance the scanner one character. '''
        self.current += 1
        return self.source[self.current-1]
    
    
    def add_token(self, token_type, literal=None):
        ''' Function to add token to self.tokens. '''
        lexeme = self.source[self.start:self.current]
        token = Token(token_type, lexeme, literal, self.line_number)
        self.tokens.append(token)
    
    
    def match_next(self, expected):
        ''' Function to match next character and consume. '''
        if self.at_end():
            return False
        elif self.source[self.current] != expected:
            return False
        else:
            self.current += 1
            return True
        
    
    def peek(self):
        ''' Function to peek the next character without consuming it. '''
        if self.current >= len(self.source):
            return '\0'
        else:
            return self.source[self.current]
        
    def peek_next(self):
        ''' Function to peek the second next character without consuming it. '''
        if self.current + 1 >= len(self.source):
            return '\0'
        else:
            return self.source[self.current+1]       
        
        
    def string(self):
        '''
        Function to handle string literals.
        
        In this scanner, multiline strings are accepted, although
        unsure if Manipula allows these.
        
        '''
        while not self.peek() == "'" and not self.at_end():
            if self.peek() == '\n':
                self.line_number += 1
            self.advance()
            
        if self.at_end():
            self.error('Untermenated string')
        
        # Consuming the closing '           
        self.advance()
        
        # Trim surrounding quotes and add token
        value = self.source[self.start+1:self.current-1]
        self.add_token(TokenType.STRING, value)
        
        
    def is_digit(self, character):
        ''' Function to determine if character is a digit. '''
        return character >= '0' and character <= '9'
    
    
    def number(self):
        ''' Function to handle number literals. '''
        while self.is_digit(self.peek()):
            self.advance()
        
        # Look for decimal place
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance() # Consume the .
            while self.is_digit(self.peek()):
                self.advance()
        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))
            
            
    def is_alpha(self, character):
        ''' Function to determine if character is alphabetical. '''
        if character >= 'a' and character <= 'z':
            return True
        elif character >= 'A' and character <= 'Z':
            return True
        elif character == '_':
            return True
        else:
            return False
        
        
    def identifier(self):
        ''' Function to handle identifier literals. '''
        while self.is_alpha_numeric(self.peek()):
            self.advance()
        
        # Create token
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text)
        if token_type == None:
            self.add_token(TokenType.IDENTIFIER)
        else:
            self.add_token(token_type)
    
        
    def is_alpha_numeric(self, character):
        ''' Function to determine if character is alphanumeric. '''
        return self.is_alpha(character) or self.is_digit(character)
        
    
    def consume_comment(self):
        ''' Function to consume a comment. '''
        while not self.peek() == '}':
            if self.at_end():
                self.error('Unmatched character "{"')
            elif self.peek() == '{':
                self.braces_counter += 1
                self.advance()
                continue
            else:
                if self.peek() == '\n': self.line_number += 1
                self.advance()
    
        
    def scan_token(self):
        '''
        Function to scan a single token, used every loop of scan_source_code().
        
        When Spyder can be used with Python 3.10 I will change
        this code to match-case statements which are much
        more efficient. For example:
        
        def f(x):
            match x:
                case 'a': return 1
                case 'b': return 2
        
        See this SO answer for a brief intro:
        https://stackoverflow.com/a/30881320/13937247
        
        In the mean time, can use two options...
        1) 
            choices = {'a': 1, 'b': 2}
            result = choices.get(key, 'default')
        2) 
            if x == 'a':
                # Do the thing
            elif x == 'b':
                # Do the other thing
            if x in 'bc':
                # Fall-through by not using elif,
                # but now the default case includes case 'a'!
            elif x in 'xyz':
                # Do yet another thing
            else:
                # Do the default            
        
        '''
        character = self.advance()
        
        # Single character tokens
        if character == '(': self.add_token(TokenType.LEFT_PAREN)
        elif character == ')': self.add_token(TokenType.RIGHT_PAREN)
        elif character == '[': self.add_token(TokenType.LEFT_SQUARE)
        elif character == ']': self.add_token(TokenType.RIGHT_SQUARE)        
        elif character == ',': self.add_token(TokenType.COMMA)
        elif character == '.': self.add_token(TokenType.DOT) 
        elif character == '-': self.add_token(TokenType.MINUS) 
        elif character == '+': self.add_token(TokenType.PLUS) 
        elif character == ';': self.add_token(TokenType.SEMICOLON)
        elif character == '/': self.add_token(TokenType.FWD_SLASH) 
        elif character == '*': self.add_token(TokenType.STAR)
        elif character == '=': self.add_token(TokenType.EQUAL_EQUAL)
        
        # Handle curley braces slightly differently as they are comments
        elif character == '{':
            self.consume_comment()
            # We are at {...
            while self.braces_counter != 0:
                self.braces_counter -= 1
                self.advance()
                self.consume_comment()
            # Consume last }
            self.advance()
        elif character == '}':
            self.error(f'Unmatched character "{character}"')       
        
        # One or two character tokens
        elif character == '!':
            if self.match_next('='):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)
        elif character == ':':
            if self.match_next('='):
                self.add_token(TokenType.EQUAL)
            else:
                self.add_token(TokenType.COLON)
        elif character == '>':
            if self.match_next('='):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif character == '<':
            if self.match_next('='):
                self.add_token(TokenType.LESS_EQUAL)
            elif self.match_next('>'):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.LESS)
                
        # Meaningless characters
        elif character == ' ': return
        elif character == '\r': return
        elif character == '\t': return
        elif character == '\n': 
            self.line_number += 1
                   
        # Literals
        elif character == "'": self.string()
        elif self.is_digit(character): self.number()
        elif self.is_alpha(character): self.identifier()
         
        # Default 
        else:
            self.error(f'Unexpected character "{character}"')
            
            
    def scan_source_code(self):
        ''' Function to scan source code and extract tokens. '''
        while not self.at_end():
            self.start = self.current
            self.scan_token()
            
        self.tokens.append(Token(TokenType.EOF, '', None, self.line_number))