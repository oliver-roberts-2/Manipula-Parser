'''
File containing the Abstract Syntax Tree (AST) printer.

'''


from expression import Visitor


class AstPrinter(Visitor):


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
    
    
    def visit_binary(expression):
        ''' Overwrites the Visitor.visit_binary() class method. '''
        return AstPrinter.parenthesise(expression.operator.lexeme,
                                       [expression.left,
                                       expression.right])


    def visit_grouping(expression):
        ''' Overwrites the Visitor.visit_grouping() class method. '''
        return AstPrinter.parenthesise('group', [expression.expression])


    def visit_literal(expression):
        ''' Overwrites the Visitor.visit_literal() class method. '''
        if expression.value == None:
            return 'None'
        else:
            return str(expression.value)


    def visit_unary(expression):
        ''' Overwrites the Visitor.visit_unary() class method. '''
        return AstPrinter.parenthesise(expression.operator.lexeme,
                                       [expression.right])

    
from expressions import Binary, Unary, Literal, Grouping
from tokens import Token, TokenType

    
expression = Binary(
    Unary(
        Token(TokenType.MINUS, '-', None, 1),
        Literal(123)
        ),
    Token(TokenType.STAR, '*', None, 1),
    Grouping(
        Literal(45.67)
        )
    )
print(AstPrinter.print_out(expression))



        
    