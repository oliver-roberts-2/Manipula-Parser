'''
File containing the parser class.

'''


from tokens import TokenType
from expression import Assign, Binary, Grouping, Literal, Unary, Variable_Expression, Logical, List
from statement import Expression, Print, Variable_Statement, If, Elif, While, For


class Parser:
    
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.had_error = False
        self.errors = []
        
    
    def parse(self):
        ''' Function to kick off parsing. '''
        statements = []
        while not self.at_end():
            statements.append(self.declaration())
        return statements
    
    
    def declaration(self):
        ''' Function to process list of declarations. '''
        try:
            if self.match([TokenType.VAR]):
                return self.var_declaration()
            else:
                return self.statement()
        except:
            return None                
    
    
    def var_declaration(self):
        ''' Function to match identifier given a VAR TokenType. '''
        name = self.consume(TokenType.IDENTIFIER, 'expect variable name')
        initialiser = None
        if self.match([TokenType.EQUAL]):
            initialiser = self.expression()
        return Variable_Statement(name, initialiser)
    
    
    def statement(self):
        ''' Function to parse one statement. '''
        if self.match([TokenType.PRINT]):
            return self.print_statement()
        elif self.match([TokenType.FOR]):
            return self.for_statement()
        elif self.match([TokenType.IF]):
            return self.if_statement()
        elif self.match([TokenType.WHILE]):
            return self.while_statement()
        else:
            return self.expression_statement()
        
    
    def for_statement(self):
        ''' Function to handle a for statement. '''
        self.consume(TokenType.LEFT_PAREN, 'expect a "(" after "while"')
        
        # Initialiser
        if self.match([TokenType.COMMA]):
            initialiser = None
        elif self.match([TokenType.VAR]):
            initialiser = self.var_declaration()
        else:
            initialiser = self.expression_statement()
        self.consume(TokenType.COMMA, 'expect "," after loop condition')
        
        # Condition
        condition = None
        if not self.check(TokenType.COMMA):
            condition = self.expression()
        self.consume(TokenType.COMMA, 'expect "," after loop condition')
        
        # Increment
        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, 'expect a ")" after condition')
        
        # Body
        body = None
        if not self.check(TokenType.ENDDO):
            body = self.statement()
        self.consume(TokenType.ENDDO, 'expect an "ENDDO" after for statement')
        return For(initialiser, condition, increment, body)
    
        
    def while_statement(self):
        ''' Function to handle a while statement. '''
        self.consume(TokenType.LEFT_PAREN, 'expect a "(" after "while"')
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, 'expect a ")" after condition')
        body = self.statement()
        return While(condition, body)
        
        
    def if_statement(self):
        ''' Function to handle an if statement. '''
        self.consume(TokenType.LEFT_PAREN, 'expect a "(" after "if"')
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, 'expect a ")" after condition')
        self.consume(TokenType.THEN, 'expect a "THEN" after condition')
        then_branch = self.statement()
        
        # Elif
        elif_list = []
        while self.match([TokenType.ELIF]):
            self.consume(TokenType.LEFT_PAREN, 'expect a "(" after "if"')
            condition = self.expression()
            self.consume(TokenType.RIGHT_PAREN, 'expect a ")" after condition')
            self.consume(TokenType.THEN, 'expect a "THEN" after condition')
            then_branch = self.statement()    
            elif_list.append(Elif(condition, then_branch))
            
        # Else
        else_branch = None
        if self.match([TokenType.ELSE]):
            else_branch = self.statement()
            
        # Consume ENDIF
        self.consume(TokenType.ENDIF, 'expect an "ENDIF" after if statement')
        return If(condition, then_branch, elif_list, else_branch)
        
        
    def print_statement(self):
        ''' Function to handle a print statement. '''
        value = self.expression()
        return Print(value)
    
    
    def expression_statement(self):
        ''' Function to handle an expression statement. '''
        expression = self.expression()
        return Expression(expression)
    
        
    def expression(self):
        ''' Function for expressions. '''
        return self.assignment()   

    # Helper Functions
    
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
            print(error_message)
        else:
            error_message = f'"{token.lexeme}" on line {token.line_number}: {message}'
            self.errors.append(error_message)
            print(error_message)
        raise Exception(error_message)
        
        # Assignment, or, and expressions
        
    def assignment(self):
        ''' Function to parse an assignment expression. '''
        expression = self._or()
        if self.match([TokenType.EQUAL]):
            equals = self.previous()
            value = self.assignment()
            if type(expression) == Variable_Expression: 
                name = expression.name
                return Assign(name, value)
            else:
                self.error(equals, 'invalid assignment target')
        return expression
                
    
    def _or(self):
        ''' Function to parse a series of or expressions. '''
        expression = self._and()
        while self.match([TokenType.OR]):
            operator = self.previous()
            right = self._and()
            expression = Logical(expression, operator, right)
        return expression
    
    
    def _and(self):
        ''' Function to parse OR operands - AND. '''
        expression = self.equality()
        while self.match([TokenType.AND]):
            operator = self.previous()
            right = self.equality()
            expression = Logical(expression, operator, right)
        return expression
                
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
        ''' Function for the comparison and IN rule. '''
        expression = self.term()
        while self.match([TokenType.GREATER, TokenType.GREATER_EQUAL,
                         TokenType.LESS, TokenType.LESS_EQUAL, TokenType.IN]):
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
        elif self.match([TokenType.IDENTIFIER]):
            return Variable_Expression(self.previous())
        elif self.match([TokenType.LEFT_PAREN]):
            expression = self.expression()
            self.consume(TokenType.RIGHT_PAREN, 'expect ")" after expression')
            return Grouping(expression)
        elif self.match([TokenType.LEFT_SQUARE]):
            sequence = [self.expression()]
            while self.match([TokenType.COMMA]):
                sequence.append(self.expression())
            self.consume(TokenType.RIGHT_SQUARE, 'expect "]" at end of list')
            return List(sequence)      
        else:
            self.error(self.peek(), 'expect expression')


    
    