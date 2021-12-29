'''
File containing the parser class.

'''


from tokens import TokenType
from expressions import Assign, Binary, Grouping, Literal, Unary


class Parser:
    
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.had_error = False
        self.errors = []
        
    
    def parse(self):
        ''' Function to kick off parsing. '''
        return self.expression()
    
    
    def peek(self):
        ''' Function to peek the next token without consuming it. '''
        return self.tokens[self.current]
    
    
    def at_end(self):
        ''' Function to determine if at end of token list. '''
        return self.peek().type == TokenType.EOF
        
    
    def previous(self):
        ''' Function to get previously consumed token. '''
        return self.tokens[self.current - 1]
        
     
    def advance(self):
        ''' Function to consume current token, otherwise return previous. '''
        if not self.at_end():
            self.current += 1
        else:
            return self.previous()

    
    def check(self, token_type):
        ''' Function to check token type. '''
        if self.at_end():
            return False
        else:
            return self.peek().type == token_type
    
    
    def match(self, types):
        '''Function to match certain token type(s) and consume it. '''
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    
    
    def consume(self, token_type, message):
        ''' Function to match a token and consme, but raise error otheriwse, '''
        if self.check(token_type):
            return self.advance()
        else:
            self.error(self.peek(), message)
            
            
    def error(self, token, message):
        ''' Function to raise error. '''
        self.had_error = True
        if token.type == TokenType.EOF:
            error_message = f'{token.type} at end {message}'
            self.errors.append(error_message)
        else:
            error_message = f'"{token.lexeme}" on line {token.line_number}: {message}'
            self.errors.append(error_message)
        raise Exception(error_message)
            
        
    # Binary Operators ...

    def equality(self):
        ''' Function for the equality rule. '''
        expression = self.comparison()
        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expression = Binary(expression, operator, right)
        return expression
    
    
    def comparison(self):
        ''' Function for the comparison rule. '''
        expression = self.term()
        while self.match([TokenType.GREATER, TokenType.GREATER_EQUAL,
                         TokenType.LESS, TokenType.LESS_EQUAL]):
            operator = self.previous()
            right = self.term()
            expression = Binary(expression, operator, right)
        return expression
    
    
    def term(self):
        ''' Function for addition and subtraction. '''
        expression = self.factor()
        while self.match([TokenType.MINUS, TokenType.PLUS]):
            operator = self.previous()
            right = self.factor()
            expression = Binary(expression, operator, right)
        return expression
    
    
    def factor(self):
        ''' Function for multiplication. '''
        expression = self.unary()
        while self.match([TokenType.FWD_SLASH, TokenType.STAR]):
            operator = self.previous()
            right = self.unary()
            expression = Binary(expression, operator, right)
        return expression
    
    # Unary Operators ...
    
    def unary(self):
        ''' Function for unary operators. '''
        if self.match([TokenType.BANG, TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        else:
            return self.primary()
        
        
    def primary(self):
        ''' Function for primary expressions. '''
        if self.match([TokenType.FALSE]): 
            return Literal(False)
        elif self.match([TokenType.TRUE]):
            return Literal(True)
        elif self.match([TokenType.NUMBER, TokenType.STRING]):
            return Literal(self.previous().literal)
        elif self.match([TokenType.LEFT_PAREN]):
            expression = self.expression()
            self.consume(TokenType.RIGHT_PAREN, 'expect ")" after expression')
            return Grouping(expression)
        else:
            print(self.peek())
            self.error(self.peek(), 'expect expression')


    def expression(self):
        ''' Function for expressions. '''
        return self.equality()
    

    
    