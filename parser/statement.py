'''
File containing the statement classes.

'''


from abc import ABC, abstractmethod


class Visitor:
    '''
    An interface that custom Visitors should implement.   
    
    '''    
    @abstractmethod
    def visit_expression(statement):
        ''' Visits Expression statements. '''
        raise NotImplementedError('Not yet implemented')
        
        
    @abstractmethod
    def visit_print(statement):
        ''' Visits Print statements. '''
        raise NotImplementedError('Not yet implemented')
        
        
    @abstractmethod
    def visit_variable_statement(statement):
        ''' Visits Variable statements. '''
        raise NotImplementedError('Not yet implemented')
        
        
    @abstractmethod
    def visit_if(statement):
        ''' Visits If statements. '''
        raise NotImplementedError('Not yet implemented')
              
        
class Statement(ABC):
    '''
    An interface the concrete objects should implement that allows the
    visitor to traverse a hierachichal structure of objects.
    
    '''
    @abstractmethod
    def accept(visitor):
        ''' The visistor traverses and accesses each object through this method. '''
        raise NotImplementedError('Not yet implemented')


class Expression(Statement):
    
    
    def __init__(self, expression):
        super().__init__()
        self.expression = expression
        
        
    def accept(self, visitor):
        return visitor.visit_expression(self)
        

class Print(Statement):
    
    
    def __init__(self, expression):
        super().__init__()
        self.expression = expression
        
        
    def accept(self, visitor):
        return visitor.visit_print(self)
         
    
class Variable_Statement(Statement):
    
    
    def __init__(self, name, initialiser):
        super().__init__()
        self.name = name
        self.initialiser = initialiser
        
        
    def accept(self, visitor):
        return visitor.visit_variable_statement(self)
    

class If(Statement):
    
    def __init__(self, condition, then_branch, else_branch):
        super().__init__()
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
        
        
    def accept(self, visitor):
        return visitor.visit_if(self)    
        
    
    
    
    
    