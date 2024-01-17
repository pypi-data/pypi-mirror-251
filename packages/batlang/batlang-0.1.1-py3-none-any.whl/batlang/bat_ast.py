class ASTNode:
    def __init__(self, type):
        self.type = type


class Expr(ASTNode):
    def __init__(self, type):
        super().__init__(type)
        
        
        
class Program(ASTNode):
    def __init__(self, type):
        self.body = []
        
        super().__init__(type)


class VarDeclaration(ASTNode):
    def __init__(self, type, identifier, value):
        self.identifier = identifier
        self.value = value
        super().__init__(type)


class AssignmentExpr(Expr):
    def __init__(self, type, assigne, value):
        self.assigne = assigne
        self.value = value
        super().__init__(type)


class Identifier(Expr):
    def __init__(self, type, symbol):
        self.symbol = symbol
        super().__init__(type)


class Numeric(Expr):
    def __init__(self, type, value):
        self.value = value
        
        super().__init__(type)
        
class String(Expr):
    def __init__(self, type, value):
        self.value = value
        super().__init__(type)     
        
class BinaryExpr(Expr):
    def __init__(self, type, left, right, op):
        self.left = left
        self.right = right
        self.op = op
        
        super().__init__(type)
        

class ConditionalExpr(Expr):
    def __init__(self, type, left, right, cond):
        self.left = left
        self.right = right
        self.cond = cond
        super().__init__(type)
        


class ConditionBlock(ASTNode):
    def __init__(self, type, if_block, elif_blocks=[], else_block=None):
        self.if_block = if_block
        self.elif_blocks = elif_blocks
        self.else_block = else_block
        
        super().__init__(type)
        
class ConditionalBlock(ASTNode):
    def __init__(self, type, conditional_expr, statements):
        self.condition = conditional_expr
        self.statements = statements
        super().__init__(type)
        

class LoopStatement(ASTNode):
    def __init__(self, type, condition):
        self.condition = condition
        self.body = []
        super().__init__(type)
        

class FunctionDeclarationStatement(ASTNode):
    def __init__(self, type, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body
        super().__init__(type)
        

class FunctionCallExpr(ASTNode):
    def __init__(self, type, name, arguments):
        self.name = name
        self.arguments = arguments
        super().__init__(type)
        

class NativeFunctionCallExpr(FunctionCallExpr):
    def __init__(self, type, name, arguments):
        super().__init__(type, name, arguments)
        

class ArrayLiteral(ASTNode):
    def __init__(self, type, name, elements):
        self.name = name
        self.elements = elements
        super().__init__(type)


class ArrayAcess(Expr):
    def __init__(self, type, name, index):
        self.name = name
        self.index = index
        super().__init__(type)