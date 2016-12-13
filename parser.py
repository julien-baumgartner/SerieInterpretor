import ply.yacc as yacc

from lex import tokens
import AST

vars = {}

def p_programme_statement(p):
    ''' programme : statement ';' '''
    p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
    ''' programme : statement ';' programme '''
    p[0] = AST.ProgramNode([p[1]]+p[3].children)

def p_statement(p):
    ''' statement : assignation-valeur
        | assignation-serie
        | structure '''
    p[0] = p[1]

def p_statement_print(p):
    ''' statement : PRINT expression '''
    p[0] = AST.PrintNode(p[2])

def p_assign_valeur(p):
    ''' assignation-valeur : IDENTIFIER '=' expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_assign_serie(p):
    ''' assignation-serie : IDENTIFIER '=' IDENTIFIER ITER IDENTIFIER ':' expression
        |  IDENTIFIER '=' IDENTIFIER ITER IDENTIFIER AS nombre ':' expression
        |  IDENTIFIER '=' FOREACH '(' IDENTIFIER ITER IDENTIFIER AS nombre ')' '{' programme '}' '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_structure(p):
    ''' structure : WHILE expression '{' programme '}'
        |  IF expression '{' programme '}'
        |  IF expression '{' programme '}' ELSE '{' programme '}' '''
    p[0] = AST.WhileNode([p[2],p[4]])

def p_expression_op(p):
    '''expression : expression ADD_OP expression
            | expression MUL_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])

def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]

def p_expression(p):
    '''expression : nombre '''
    p[0] = AST.TokenNode(p[1])

def p_nombre(p):
    ''' nombre : NUMBER
        | IDENTIFIER
        | IDENTIFIER '[' nombre ']' '''
    p[0] = AST.TokenNode(p[1])





def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Sytax error: unexpected end of file!")


precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog, debug=1)
    if result:
        print (result)
    else:
        print ("Parsing returned no result!")
