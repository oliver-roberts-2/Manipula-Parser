'''
File containing the interpreter class.

'''


class Interpreter:
    
    
    def __init__(self):
        pass
    
    
    def evaluate(self, expression):
        ''' Function to evaluate an expression. '''
        return expression.accept()
    
    
    def visit_literal(self, literal):
        return literal.value
    
    
    def visit_grouping(self, grouping):
        return self.evaluate(grouping.expression)

