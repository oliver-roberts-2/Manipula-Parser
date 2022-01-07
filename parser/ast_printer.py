'''
File containing the Abstract Syntax Tree (AST) printer.

'''


from expression import Visitor as Expression_Visitor
from statement import Visitor as Statement_Visitor
from expression import Expression
from statement import Statement
from tokens import Token


class AstPrinter(Expression_Visitor, Statement_Visitor):


    def print_out(expression):
        return expression.accept(AstPrinter)
       
    
    def parenthesise(name, expressions):
        '''
        Function that takes a name and list of subexpressions and
        wraps them in parenthesise for printing.

        Parameters
        ----------
        name : str
            Name of operation.
        expressions : list of expressions
            List of epxressions to parenthesise.

        Returns
        -------
        str
            String representation of the parenthesised group.

        '''
        string_list = ['(', name]
        for expression in expressions:
            string_list.append(' ')
            string_list.append(expression.accept(AstPrinter))
        string_list.append(')')
        return ''.join(string_list)
    
    
    def parenthesise2(name, parts):
        '''
        Function that takes a name and list of parts and
        wraps them in parenthesise for printing.

        Parameters
        ----------
        name : str
            Name of operation.
        parts : list of objects
            List of parts to parenthesise.

        Returns
        -------
        str
            String representation of the parenthesised group.

        '''
        string_list = ['(', name]
        string_list = AstPrinter.transform(string_list, parts)
        string_list.append(')')
        print(string_list)
        return ''.join(string_list)
    
    
    def transform(string_list, parts):
        ''' Transforms list of parts into parenthasises expressions/statments. '''
        for part in parts:
            string_list.append(' ')
            if isinstance(part, Expression):
                string_list.append(part.accept(AstPrinter))
            elif isinstance(part, Statement):
                string_list.append(part.accept(AstPrinter))
            elif isinstance(part, Token):
                string_list.append(part.lexeme)
            elif isinstance(part, list):
                AstPrinter.transform(string_list, part)
            else:
                print('Else is happening')
                string_list.append(part)
        return string_list
                
   
    
    # Expressions
    
    def visit_binary(expression):
        ''' Overwrites the Expression.visit_binary() class method. '''
        return AstPrinter.parenthesise(expression.operator.lexeme,
                                       [expression.left,
                                       expression.right])


    def visit_grouping(expression):
        ''' Overwrites the Expression.visit_grouping() class method. '''
        return AstPrinter.parenthesise('group', [expression.expression])


    def visit_literal(expression):
        ''' Overwrites the Expression.visit_literal() class method. '''
        if expression.value == None:
            return 'None'
        else:
            return str(expression.value)
        
        
    def visit_variable_expression(expression):
        ''' Overwrites the Expression.visit_variable_expression() class method. '''
        return expression.name.lexeme


    def visit_unary(expression):
        ''' Overwrites the Expression.visit_unary() class method. '''
        return AstPrinter.parenthesise(expression.operator.lexeme,
                                       [expression.right])

    # Statments
    
    def visit_expression_statement(statement):
        ''' Overwrites the Statement.visit_expression_statement() class method.'''
        return AstPrinter.parenthesise(';', [statement.expression])
        
    
    def visit_if(statement):
        ''' Overwrites the Statement.visit_if() class method.'''
        if statement.else_branch == None:
            return AstPrinter.parenthesise2('if', [statement.condition,
                                                  statement.then_branch])
        else:
            return AstPrinter.parenthesise2('if-else', [statement.condition,
                                                       statement.then_branch,
                                                       statement.else_branch])
        
        
    def visit_for(statement):
        ''' Overwrites the Statement.visit_for() class method. '''
        return AstPrinter.parenthesise2('for', [statement.condition,
                                               statement.body])
    
    
    def visit_print(statement):
        ''' Overwrites the Statement.visit_print() class method.'''
        return AstPrinter.parenthesise('print', [statement.expression])
    
    
    def visit_variable_statement(statement):
        ''' Overwrites the Statement.visit_variable_statement() class method.'''
        if statement.initialiser == None:
            return AstPrinter.parenthesise2('var', [statement.name])
        else:
            return AstPrinter.parenthesise2('var', [statement.name,
                                                    '=',
                                                    statement.initialiser])

        
    