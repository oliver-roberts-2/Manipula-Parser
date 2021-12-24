'''
File containing the expression classes.

'''


class Expression:
    
    
    def __init__(self):
        pass
    
    
class Assign(Expression):
    
    
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value
        

class Binary(Expression):
    
    
    def __init__(self, left, operator, right):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right
        
    def __repr__(self):
        return f'{self.left} {self.operator} {self.right}'
        
        
class Grouping(Expression):
    
    
    def __init__(self, expression):
        super().__init__()
        self.expression = expression
        

class Literal(Expression):
    
    
    def __init__(self, value):
        super().__init__()
        self.value = value


class Unary(Expression):
    
    
    def __init__(self, operator, right):
        super().__init__()
        self.operator = operator
        self.right = right
        
         
        