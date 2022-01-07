'''
File containing the interpreter class.

'''


from expression import Visitor as Expression_Visitor
from statement import Visitor as Statement_Visitor


class PythonPrinter(Expression_Visitor, Statement_Visitor):
    
    
    def _write(statements):
        ''' Function to interpret and execute a list of statements. '''
        for statement in statements:
            PythonPrinter.execute(statement)

            
    def execute(statement):
        ''' Function to send statements back into the interpreter's visitor implementation. '''
        statement.accept(PythonPrinter)
            
    
    def evaluate(expression):
        ''' Function to send expression back into the interpreter's visitor implementation. '''
        return expression.accept(PythonPrinter)
    
    
# =============================================================================
# Statements
# =============================================================================
       
    
    def visit_expression_statement(statement):
        ''' Overwrites Statement.visit_expression_statement() class method. '''
        return PythonPrinter.evaluate(statement.expression)
        
        
    def visit_print(statement):
        ''' Overwrites Statement.visit_print() class method. '''
        value = PythonPrinter.evaluate(statement.expression) 
        return f'print({value})'
        
    def visit_variable_statement(statement):
        ''' Overwrites Statement.visit_variable_statement() class method. '''       
        value = None
        if statement.initialiser != None:
            value = PythonPrinter.evaluate(statement.initialiser)
        return f'{statement.name.lexeme} = {value}'        
        
    def visit_if(statement):
        ''' Overwrites Statement.visit_if() class method. '''
        raise NotImplementedError('Not yet implemented')
        
        
    def visit_elif(statement):
        ''' Overwrites Statement.visit_elif() class method. '''
        raise NotImplementedError('Not yet implemented')
        
        
    def visit_while(statement):
        ''' Overwrites Statement.visit_while() class method. '''
        raise NotImplementedError('Not yet implemented')
        
        
    def visit_for(statement):
        ''' Overwrites Statement.visit_for() class method. '''
        raise NotImplementedError('Not yet implemented')
    
    
# =============================================================================
# Expressions
# =============================================================================
    
    
    def visit_binary(expression):
        ''' Overwrites Expression.visit_binary() class method. '''
        left = PythonPrinter.evaluate(expression.left)
        right = PythonPrinter.evaluate(expression.right)
        return f'{left} {expression.operator.lexeme} {right}'
        

    def visit_grouping(expression):
        ''' Overwrites Expression.visit_grouping() class method. '''
        group = PythonPrinter.evaluate(expression.expression)
        return f'({group})'

    
    def visit_literal(expression):
        ''' Overwrites Expression.visit_literal() class method. '''
        return str(expression.value)
     
      
    def visit_unary(expression):
        ''' Overwrites Expression.visit_unary() class method. '''
        right = PythonPrinter.evaluate(expression.right)
        operator = expression.operator.lexeme
        return f'{operator}{right}'
    
    
    def visit_variable_expression(expression):
        ''' Overwrites Expression.visit_variable_expression() class method. '''
        var_name = PythonPrinter.evaluate(expression.name)
        return str(var_name.lexeme)
        

    def visit_multi_identifier_variable_expression(expression):
        '''Overwrites Expression.visit_multi_identifier_variable_expression() class method. '''
        return ''.join(expression.names)
        

    def visit_assign(expression):
        ''' Overwrites Expression.visit_assign() class method. '''
        value = PythonPrinter.evaluate(expression.value)
        return str(value)
        
    
    def visit_logical(expression):
        ''' Overwrites Expression.visit_logical() class method. '''
        return f'{expression.left} {expression.operator.lexeme} {expression.right}'        
        
    
    def visit_list(expression):
        ''' Overwrites Expression.visit_list() class method. '''
        elements = [PythonPrinter.evaluate(expr) for expr in expression.sequence]
        return f'[{", ".join(elements)}]'
        
        
    def visit_range(expression):
        ''' Overwrites Expression.visit_range() class method. '''
        lower = PythonPrinter.evaluate(expression.lower)
        upper = PythonPrinter.evaluate(expression.upper)
        return f'range({lower}, {upper})'

        