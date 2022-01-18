'''
File containing the interpreter class.

'''


from tokens import Token
from expression import Visitor as Expression_Visitor
from expression import Range, Variable_Expression
from statement import Visitor as Statement_Visitor


class PythonPrinter(Expression_Visitor, Statement_Visitor):
    
    
    indent = 0
    
    
    def _write(statements):
        ''' Function to interpret and execute a list of statements. '''
        python_syntax = []
        for statement in statements:
            python_syntax.append(PythonPrinter.execute(statement))
        return python_syntax

            
    def execute(statement):
        ''' Function to send statements back into the printer's visitor implementation. '''
        if isinstance(statement, list):
            for stmt in statement:
                return stmt.accept(PythonPrinter)
        else:
            return statement.accept(PythonPrinter)
            
    
    def evaluate(expression):
        ''' Function to send expression back into the printer's visitor implementation. '''
        return expression.accept(PythonPrinter)
    
    
    def stringify(an_object):
        ''' Function to convert an object to a string. '''
        if an_object == None:
            return 'None'
        else:
            return str(an_object)
    
    
# =============================================================================
# Statements
# =============================================================================
       
    
    def visit_expression_statement(statement):
        ''' Overwrites Statement.visit_expression_statement() class method. '''
        return PythonPrinter.evaluate(statement.expression)
        
        
    def visit_print(statement):
        ''' Overwrites Statement.visit_print() class method. '''
        value = PythonPrinter.evaluate(statement.expression)
        if isinstance(statement.expression, Variable_Expression):
            return f'print({value})'
        else:
            return f'print("{value}")'
        
        
    def visit_variable_statement(statement):
        ''' Overwrites Statement.visit_variable_statement() class method. '''
        name = PythonPrinter.evaluate(statement.name)
        if statement.initialiser != None:
            value = PythonPrinter.evaluate(statement.initialiser)
            if isinstance(statement.initialiser, Range):
                return f'{name} in {value}'
            else:
                return f'{name} = {value}'
        else:
            return f'{name}' 
        
        
    def visit_if(statement):
        ''' Overwrites Statement.visit_if() class method. '''
        condition = PythonPrinter.evaluate(statement.condition)
        # string = '\n' + '\t'*PythonPrinter.indent
        string = f'if {condition}:'
        
        PythonPrinter.indent += 1
        # Then branch
        for stmt in statement.then_branch:
            string += '\n' + '\t'*PythonPrinter.indent
            then_branch = PythonPrinter.execute(stmt)
            string += then_branch
        
        
        # Elif branch
        if statement.elif_branch != []:
            for stmt in statement.elif_branch:
                elif_branch = PythonPrinter.execute(stmt)
                PythonPrinter.indent -= 1
                string += '\n' + '\t'*PythonPrinter.indent
                PythonPrinter.indent += 1
                string += elif_branch.replace('\t', '\t'*PythonPrinter.indent)
        
        # Else branch 
        if statement.else_branch != None:
            else_branch = PythonPrinter.execute(statement.else_branch)
            PythonPrinter.indent -= 1
            string += '\n' + '\t'*PythonPrinter.indent + 'else:'
            PythonPrinter.indent += 1
            string += '\n' + '\t'*PythonPrinter.indent + else_branch
        
        PythonPrinter.indent -= 1
        return string
        
        
    def visit_elif(statement):
        ''' Overwrites Statement.visit_elif() class method. '''
        condition = PythonPrinter.evaluate(statement.condition)
        then_branch = PythonPrinter.execute(statement.then_branch)
        return f'elif {condition}:' + '\n\t' + f'{then_branch}'

        
    def visit_while(statement):
        ''' Overwrites Statement.visit_while() class method. '''
        condition =  PythonPrinter.evaluate(statement.condition)
        body =  PythonPrinter.execute(statement.body)
        return f'while {condition}: {body}'
        
        
    def visit_for(statement):
        ''' Overwrites Statement.visit_for() class method. '''
        initialiser = PythonPrinter.evaluate(statement.initialiser)
        string = f'for {initialiser}:'
        PythonPrinter.indent += 1
        for stmt in statement.body:
            body = PythonPrinter.execute(stmt)
        # Body
            string += '\n' + '\t'*PythonPrinter.indent + f'{body}'
        
        PythonPrinter.indent -= 1
        return string
    
    
# =============================================================================
# Expressions
# =============================================================================
    
    
    def visit_binary(expression):
        ''' Overwrites Expression.visit_binary() class method. '''
        left = PythonPrinter.evaluate(expression.left)
        right = PythonPrinter.evaluate(expression.right)
        return f'{left} {expression.operator.type.value} {right}'
        

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
        name = expression.name
        if isinstance(name, Token):
            return name.lexeme
        else:
            return PythonPrinter.evaluate(name)
        

    def visit_multi_identifier_variable_expression(expression):
        '''Overwrites Expression.visit_multi_identifier_variable_expression() class method. '''
        elements = [token.lexeme for token in expression.names]
        return ''.join(elements)
        

    def visit_assign(expression):
        ''' Overwrites Expression.visit_assign() class method. '''
        name = PythonPrinter.evaluate(expression.name)
        value = PythonPrinter.evaluate(expression.value)
        return f'{name} = {value}'
        
    
    def visit_logical(expression):
        ''' Overwrites Expression.visit_logical() class method. '''
        left = PythonPrinter.evaluate(expression.left)
        right = PythonPrinter.evaluate(expression.right)
        return f'{left} {expression.operator.type.value} {right}'        
        
    
    def visit_list(expression):
        ''' Overwrites Expression.visit_list() class method. '''
        elements = [PythonPrinter.evaluate(expr) for expr in expression.sequence]
        return '{' + ', '.join(elements) + '}'
        
        
    def visit_range(expression):
        ''' Overwrites Expression.visit_range() class method. '''
        lower = PythonPrinter.evaluate(expression.lower)
        upper = PythonPrinter.evaluate(expression.upper)
        return f'range({lower}, {upper})'

        