'''
File containing the interpreter class.

'''


from expressions import Visitor
from tokens import TokenType


class Interpreter(Visitor):
    
    
    def interpret(expression):
        ''' Function to evaluate a syntax tree expression. '''
        try:
            value  = Interpreter.evaluate(expression)
            print(Interpreter.stringify(value))
        except:
            raise RuntimeError()
            
            
    def stringify(an_object):
        ''' Convert value to a string. '''
        if an_object == None:
            return 'None'
        elif type(an_object) == float:
            return str(an_object)
        else:
            return str(an_object)
    
    
    def evaluate(expression):
        ''' Function to send expression back into the interpreter's visitor implementation. '''
        return expression.accept(Interpreter)
    
    
    def is_truthy(an_object):
        ''' 
        Function to determine the truth of an object.
        
        Here, false and None are falsey; everything else is truthy. 
        
        '''
        if an_object == None:
            return False
        elif type(an_object) == bool:
            return an_object
        else:
            return True
    
    
    def is_equal(a, b):
        ''' Function to determine if a and b are equal. '''
        if a == None and b == None:
            return True
        elif a == None:
            return False
        else:
            return a == b
        
        
    def check_number_operand(operator, operand):
        ''' Function to check an object's type. '''
        if type(operand) == float:
            return
        else:
            raise RuntimeError(f'{operator} operand must be a number')
            
            
    def check_number_operands(operator, left, right):
        ''' Function to check two objects'' type. '''
        if type(left) == float and type(right) == float:
            return
        else:
            raise RuntimeError(f'{operator} operands must be numbers')
    
    
    def visit_binary(expression):
        ''' Overwrites the Visitor.visit_binary() class method. '''
        left = Interpreter.evaluate(expression.left)
        right = Interpreter.evaluate(expression.right)
        
        if expression.operator.type == TokenType.MINUS:
            Interpreter.check_number_operands(expression.operator, left, right)
            return left - right
        
        # Handles special case of + where can be used to concat strings
        elif expression.operator.type == TokenType.PLUS:
            if type(left) == float and type(right) == float:
                return float(left) + float(right)
            elif type(left) == str and type(right) == str:
                return str(left) + str(right)
            else:
                print('Unknown or mismatched types() of left and right expressions.'\
                      f'Left is type {type(left)}, right is type {type(right)}.')
                raise RuntimeError(f'{expression.operator} operands must be two numbers or two strings')
        elif expression.operator.type == TokenType.FWD_SLASH:
            Interpreter.check_number_operands(expression.operator, left, right)
            return left / right
        elif expression.operator.type == TokenType.STAR:
            Interpreter.check_number_operands(expression.operator, left, right)
            return left * right
        
        # Comparison operators
        elif expression.operator.type == TokenType.GREATER:
            Interpreter.check_number_operands(expression.operator, left, right)
            return left > right
        elif expression.operator.type == TokenType.GREATER_EQUAL:
            Interpreter.check_number_operands(expression.operator, left, right)
            return left >= right
        elif expression.operator.type == TokenType.LESS:
            Interpreter.check_number_operands(expression.operator, left, right)
            return left < right
        elif expression.operator.type == TokenType.LESS_EQUAL:
            Interpreter.check_number_operands(expression.operator, left, right)
            return left <= right
        
        # Comparison Operators
        elif expression.operator.type == TokenType.BANG_EQUAL:
            return not Interpreter.is_equal(left, right)
        elif expression.operator.type == TokenType.EQUAL_EQUAL:
            return Interpreter.is_equal(left, right)
        
        # Default
        else:
            return None


    def visit_grouping(expression):
        ''' Overwrites the Visitor.visit_grouping() class method. '''
        return Interpreter.evaluate(expression.expression)


    def visit_literal(expression):
        ''' Overwrites the Visitor.visit_literal() class method. '''
        return expression.value


    def visit_unary(expression):
        ''' Overwrites the Visitor.visit_unary() class method. '''
        right = Interpreter.evaluate(expression.right)
        if expression.operator.type == TokenType.MINUS:
            Interpreter.check_number_operand(expression.operator, right)
            return -right
        elif expression.operator.type == TokenType.BANG:
            return not Interpreter.is_truthy(right)
        else:
            return None
        
    
    
    
