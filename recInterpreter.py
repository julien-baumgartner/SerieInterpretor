import AST
from AST import addToClass
from functools import reduce

operations = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '*' : lambda x,y: x*y,
    '/' : lambda x,y: x/y,
}

values ={}
series ={}

//{x,}

class Serie:
    def __init__(self, sx, sy, start, expression):
        self.sx = sx
        self.sy = sy
        self.start = start

        self.values = []
        self.expression = expression

    def execute(self, others, index):
        if(len(self.values) > index):
            return self.values[index]
        else:
            x = 0;
            self.values = []
            newVars = { self.sx => x,
                        self.sy => values[x-1] if x > 0 else start,
                        "others" => others}
            while x < index:
                values[x] = expression.execute(newVars)

@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()

@addToClass(AST.AssignValueNode)
def execute(self):
    values[self.children[0].tok] = self.children[1].execute()

@addToClass(AST.AssignSerieNode)
def execute(self, others):
    sx = self.children[0].tok
    sy = self.children[1].tok
    start = self.children[2].execute(others)
    expression = self.
    series[self.children[0].tok] = Serie()

@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print ("*** Error: variable %s undefined!" % self.tok)
    return self.tok

@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0,0)
    return reduce(operations[self.op], args)


@addToClass(AST.PrintNode)
def execute(self):
    print (self.children[0].execute())

@addToClass(AST.WhileNode)
def execute(self):
    while(self.children[0].execute()):
        self.children[1].execute()

if __name__ == "__main__":
    from parser5 import parse
    import sys
    prog = open(sys.argv[1]).read()
    ast = parse(prog)

    ast.execute()
