'''
File containing the Abstract Syntax Tree (AST) printer.

'''


from expressions import Visitor


class AstPrinter(Visitor):


    def print_out(expression):
        return expression.accept()
       
    
    def parenthesise(name, expressions):
        ''' Function that takes a name and list of subexpressions and wraps in (). '''
        string_list = ['(', name]
        for expression in expressions:
            string_list.append(' ')
            string_list.append(expression.accept())
        string_list.append(')')
        print(string_list)
        return ''.join(string_list)
    
    
    def visit_binary(expression):
        return AstPrinter.parenthesise(expression.operator.lexeme,
                                       expression.left,
                                       expression.right)


    def visit_grouping(expression): 
        return AstPrinter.parenthesise('group', expression.expression)


    def visit_literal(expression):
        if expression.value == None:
            return 'None'
        else:
            return str(expression.value)


    def visit_unary(expression):
        return AstPrinter.parenthesise(expression.operator.lexeme,
                                       expression.right)

    
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
AstPrinter.print_out(expression)



        
    