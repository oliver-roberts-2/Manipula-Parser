'''
File containing the expression classes.

'''


from abc import ABC, abstractmethod


class Visitor:
    '''
    An interface that custom Visitors should implement.   
    
    '''          
    @abstractmethod
    def visit_binary(expression):
        ''' Visits binary expressions. '''
        raise NotImplementedError('Not yet implemented')
        

    @abstractmethod
    def visit_grouping(expression):
        ''' Visits grouping expressions. '''
        raise NotImplementedError('Not yet implemented')

    
    @abstractmethod
    def visit_literal(expression):
        ''' Visits literal expressions. '''
        raise NotImplementedError('Not yet implemented')
     
      
    @abstractmethod
    def visit_unary(expression):
        ''' Visits unary expressions. '''
        raise NotImplementedError('Not yet implemented')
        
    
    @abstractmethod
    def visit_variable_expression(expression):
        ''' Visits variable expressions. '''
        raise NotImplementedError('Not yet implemented')
        

    @abstractmethod
    def visit_multi_identifier_variable_expression(expression):
        ''' Visits multi-identifier variable expressions. '''
        raise NotImplementedError('Not yet implemented')
        

    @abstractmethod
    def visit_assign(expression):
        ''' Visits assign expressions. '''
        raise NotImplementedError('Not yet implemented')
        
        
    @abstractmethod
    def visit_logical(expression):
        ''' Visits logical expressions. '''
        raise NotImplementedError('Not yet implemented')
        
        
    @abstractmethod
    def visit_list(expression):
        ''' Visits list expressions. '''
        raise NotImplementedError('Not yet implemented')
        
        
    @abstractmethod
    def visit_range(expression):
        ''' Visits range expressions. '''
        raise NotImplementedError('Not yet implemented')
       
        
class Expression(ABC):
    '''
    An interface the concrete objects should implement that allows the
    visitor to traverse a hierachichal structure of objects.
    
    '''
    @abstractmethod
    def accept(visitor):
        ''' The visistor traverses and accesses each object through this method. '''
        raise NotImplementedError('Not yet implemented')
       

class Binary(Expression):
    
    
    def __init__(self, left, operator, right):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right
        
    def __repr__(self):
        return f'{self.left} {self.operator} {self.right}'
    
    
    def accept(self, visitor):
        return visitor.visit_binary(self)
        
        
class Grouping(Expression):
    
    
    def __init__(self, expression):
        super().__init__()
        self.expression = expression
        
    
    def accept(self, visitor):
        return visitor.visit_grouping(self)    
        

class Literal(Expression):
    
    
    def __init__(self, value):
        super().__init__()
        self.value = value


    def accept(self, visitor):
        return visitor.visit_literal(self)
    

class Unary(Expression):
    
    
    def __init__(self, operator, right):
        super().__init__()
        self.operator = operator
        self.right = right
        
        
    def accept(self, visitor):
        return visitor.visit_unary(self) 
    
    
class Variable_Expression(Expression):
    
    
    def __init__(self, name):
        super().__init__()
        self.name = name
        
        
    def accept(self, visitor):
        return visitor.visit_variable_expression(self)
    
    
class Multi_Identifier_Variable_Expression(Expression):
    

    def __init__(self, names):
        super().__init__()
        self.names = names # Must be a list 
        
        
    def accept(self, visitor):
        return visitor.visit_multi_identifier_variable_expression(self)
    
    
class Assign(Expression):
    
    
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value
        
        
    def accept(self, visitor):
        return visitor.visit_assign(self)
    
    
class Logical(Expression):
    
    
    def __init__(self, left, operator, right):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right
        
        
    def accept(self, visitor):
        return visitor.visit_logical(self)   
    

class List(Expression):

    
    def __init__(self, sequence):
        super().__init__()
        self.sequence = sequence

        
    def accept(self, visitor):
        return visitor.visit_list(self)

        
class Range(Expression):

    
    def __init__(self, lower, upper):
        super().__init__()
        self.lower = lower
        self.upper = upper

        
    def accept(self, visitor):
        return visitor.visit_range(self)
         
        