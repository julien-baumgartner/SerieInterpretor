import AST
from AST import addToClass
from functools import reduce
from myparser import parse

operations = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '*' : lambda x,y: x*y,
    '/' : lambda x,y: x/y,
}

class Serie:
    def __init__(self, sx, sy, start, expression, execution):
        self.sx = sx
        self.sy = sy
        self.start = start

        self.values = []
        self.expression = expression
        self.execution = execution

    def execute(self, others, index):
        if(len(self.values) > index):
            return self.values[index]
        else:
            return self.execution(self, others, index)

    def executeLambda(self, others, index):
        x = 0
        self.values = []
        newVars = { self.sx : x,
                    self.sy : values[x-1] if x > 0 else self.start,
                    "others" : others}
        while newVars[self.sx] <= index:
            newVars[self.sy] = self.expression.execute(newVars)
            self.values.append(newVars[self.sy])
            newVars[self.sx] += 1

        return self.values[-1]

    def executeForeach(self, others, index):
        x = 0
        self.values = []
        newVars = { self.sx : x,
                    self.sy : values[x-1] if x > 0 else self.start,
                    "others" : others}
        while newVars[self.sx] <= index:
            self.expression.execute(newVars)
            self.values.append(newVars[self.sy])
            newVars[self.sx] += 1

        return self.values[-1]

@addToClass(AST.ProgramNode)
def execute(self, others):
    for c in self.children:
        c.execute(others)

@addToClass(AST.AssignValueNode)
def execute(self, others):
    others[self.children[0].tok] = self.children[1].execute(others)

@addToClass(AST.AssignSerieNode)
def execute(self, others):
    defNode = self.children[1]
    sx = defNode.children[0].tok
    sy = defNode.children[1].tok
    start = defNode.children[2].execute(others)
    expression = self.children[2]
    others[self.children[0].tok] = Serie(sx,sy,start,expression, Serie.executeLambda)

@addToClass(AST.TokenNode)
def execute(self, others):
    gOthers = others
    if isinstance(self.tok, str):
        while True:
            if self.tok in others.keys():
                try:
                    if  isinstance(others[self.tok], Serie):
                        return others[self.tok].execute(gOthers, int(self.children[0].execute(gOthers)))
                    else:
                        return others[self.tok]
                except KeyError:
                    print ("*** Error: variable %s undefined!" % self.tok)
            if("others" in others.keys()):
                others = others["others"]
            else:
                break
    return self.tok

@addToClass(AST.OpNode)
def execute(self, others):
    args = [c.execute(others) for c in self.children]
    if len(args) == 1:
        args.insert(0,0)
    return reduce(operations[self.op], args)


@addToClass(AST.PrintNode)
def execute(self, others):
    print (self.children[0].execute(others))

@addToClass(AST.WhileNode)
def execute(self, others):
    while(self.children[0].execute(others)):
        self.children[1].execute(others)

@addToClass(AST.ForeachNode)
def execute(self, others):
    defNode = self.children[1]
    sx = defNode.children[0].tok
    sy = defNode.children[1].tok
    start = defNode.children[2].execute(others)
    expression = self.children[2]
    others[self.children[0].tok] = Serie(sx,sy,start,expression, Serie.executeForeach)

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()
    ast = parse(prog)

    others = {}
    ast.execute(others)
