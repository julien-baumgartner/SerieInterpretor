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
    p[0] = AST.AssignValueNode([AST.TokenNode(p[1]),p[3]])

def p_assign_serie(p):
    ''' assignation-serie : IDENTIFIER '=' def-iter ':' expression
        |  IDENTIFIER '=' FOREACH '(' def-iter ')' '{' programme '}' '''
    if len(p) == 6:
        p[0] = AST.AssignSerieNode([AST.TokenNode(p[1]),p[3],p[5]])
    elif len(p) == 10:
        p[0] = AST.ForeachNode([AST.TokenNode(p[1]),p[5],p[8]])


def p_def_iter(p):
    ''' def-iter : IDENTIFIER ITER IDENTIFIER
        |  IDENTIFIER ITER IDENTIFIER AS expression'''
    nombre = p[5] if len(p) == 6 else AST.TokenNode(0)
    p[0] = AST.DefIterNode([AST.TokenNode(p[1]),AST.TokenNode(p[3]), nombre])

def p_structure(p):
    ''' structure : WHILE expression '{' programme '}'
        |  IF expression '{' programme '}'
        |  IF expression '{' programme '}' ELSE '{' programme '}' '''
    print(p[1])
    if(p[1].upper() == 'WHILE'):
        p[0] = AST.WhileNode([p[2],p[4]])
    elif(p[1].upper() == 'IF'):
        if(len(p) == 6):
            p[0] = AST.ConditionNode([p[2],p[4]])
        elif(len(p) == 10):
            p[0] = AST.ConditionNode([p[2],p[4],p[8]])

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
    ''' expression : NUMBER
        | IDENTIFIER
        | IDENTIFIER '[' expression ']' '''
    if len(p) == 2:
        p[0] = AST.TokenNode(p[1])
    elif len(p) == 5:
        p[0] = AST.SerieTokenNode(p[1],[p[3]])





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
    import sys, os
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog, debug=1)
    print (result)
    graph = result.makegraphicaltree()
    name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
    graph.write_pdf(name)
    print("wrote ast to", name)
