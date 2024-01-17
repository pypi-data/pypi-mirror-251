from batlang.bat_values import *
import sys
from batlang.bat_env import Environment, create_global_env
from batlang.bat_lexer import Lexer
from batlang.bat_parser import Parser

types = ("number", "string")

def interpret_program(program, env):
    interpreted = []
    for statement in program.body:
        curr = interpret(statement, env)
        if curr:
            interpreted.append(curr)
    
    return interpreted

def interpret_binary_expr(binary_expr, env):
    left = interpret(binary_expr.left, env)
    right = interpret(binary_expr.right, env)
    
    if(left.type == "number" and right.type == "number"):
        return interpret_numeric_expr(left, right, binary_expr.op)
    
    elif(left.type in types and right.type in types):
        if binary_expr.op == "+":
            return StringVal("string", left.value + right.value)
    
    return mk_null()


def interpret_condition_block(condition_block, env):
    if_block = condition_block.if_block
    elif_blocks = condition_block.elif_blocks
    else_block = condition_block.else_block
    
    
    if_condition = interpret_conditional_expr(if_block.condition, env).value
    elif_condition = False
    else_condition = True if else_block else False
    elif_block = None
    
    if elif_blocks:
        for block in elif_blocks:
            elif_condition = interpret_conditional_expr(block.condition, env).value
            
            if elif_condition == True:
                elif_block = block
                break
    
    
    if if_condition == True:
        for statement in if_block.statements:
            interpret(statement, env)
     
    if elif_condition == True and elif_block != None:
        for statement in elif_block.statements:
            interpret(statement, env)
        
    elif else_condition == True:
        for statement in else_block.statements:
            interpret(statement, env)
            

def interpret_loop_statement(loop, env):
    condition = interpret_conditional_expr(loop.condition, env).value
    while condition:
        for statement in loop.body:
            # NOTE: this is temporary
            interpret(statement, env)
        condition = interpret_conditional_expr(loop.condition, env).value 
    
    return condition
    

def interpret_conditional_expr(conditional_expr, env):
    left = interpret(conditional_expr.left, env)
    right = interpret(conditional_expr.right, env)
    
    if(left.type in types and right.type in types):
        return interpret_conditions(left, right, conditional_expr.cond)

def interpret_conditions(left, right, cond):
    result = None
    env = create_global_env()
    match cond:
        case ">":
            result = left.value > right.value
        case "<":
            result = left.value < right.value
        case "==":
            result = left.value == right.value
        case "<=":
            result = left.value <= right.value
        case ">=":
            result = left.value >= right.value
        case "!=":
            result = left.value != right.value
        case _:
            result = "Condition Not Recognized"
    
    return ConditionalVal(value=result, type="conditional")
        

def interpret_numeric_expr(left, right, op):
    result = 0
    
    if(op == "+"):
        result = left.value + right.value
    elif(op == "-"):
        result = left.value - right.value
    elif(op == "*"):
        result = left.value * right.value
    elif(op == "/"):
        result = left.value / right.value
    else:
        result = left.value % right.value
        
    return NumberVal(value=result, type="number")


def interpret_identifier(identifier, env):
    val = env.lookup_var(identifier.symbol)
    return val

def interpret_var_declaration(declaration, env):
    value = interpret(declaration.value, env)
    return env.declare_var(declaration.identifier, value)

def interpret_assignment(node, env):
    if(node.assigne.type != "Identifier"):
        print(f"Invalid assignment inside assignment expression {node.assigne}")
    
    name = node.assigne.symbol
    return env.assign_var(name, interpret(node.value, env))


def interpret_function_declaration(declaration, env):
    fn = FunctionValue("function", declaration.name, declaration.parameters, env, declaration.body)
    
    return env.declare_var(declaration.name, fn)


def interpret_function_call_expr(call, env):
    fn = env.lookup_var(call.name)
    scope = Environment(fn.env)
    args = []
    
    for arg in call.arguments:
        args.append(interpret(arg, env))
    
    i = 0
    while i < len(fn.parameters):
        var_name = fn.parameters[i].symbol
        scope.declare_var(var_name, args[i])
        i += 1
        
    result = mk_null()
    
    for stmt in fn.body:
        if(isinstance(stmt, tuple)):
            result = interpret(stmt[0], scope)
            continue
        interpret(stmt, scope)
    
    return result
    
def interpret_native_function_call_expr(call, env):
    match call.name:
        case "batSignal":
            args = []
            for arg in call.arguments:
                args.append(interpret(arg, env))
                
            for arg in args:
                print(arg.value)
        case "batDirective":
            prompt = input()
            try:
                try:
                    value = int(prompt)
                    return NumberVal("number", value)
                except:
                    value = float(prompt)
                    return NumberVal("number", value)
            except:
                value = str(prompt)
                return StringVal(type="string", value=value)



def interpret_number_val(ASTNode):
    number = None
    
    try:
        number = int(ASTNode.value)
    except:
        number = float(ASTNode.value)
    
    return NumberVal("number", number)

def interpret_array_declaration(arr, env):
    elements = []
    
    for element in arr.elements:
        elements.append(interpret(element, env).value)
    
    arr_val = ArrayLiteralValue("array", arr.name, elements)
    
    env.declare_var(arr.name, arr_val)

def interpret_array_call_expr(call, env):
    array = env.lookup_var(call.name)
    
    val = array.value[int(call.index)]
    
    return ArrayMember("array_member", val)


def interpret(ASTNode, env):
    if(ASTNode == None):
        return
    match ASTNode.type:
        case "Identifier":
            return interpret_identifier(ASTNode, env)
        case "Numeric":
            return interpret_number_val(ASTNode)
        case "String":
            return StringVal("string", ASTNode.value)
        case "BinaryExpr":
            return interpret_binary_expr(ASTNode, env)
        case "ConditionalExpr":
            return interpret_conditional_expr(ASTNode, env)
        case "Program":
            return interpret_program(ASTNode, env)
        case "VarDeclaration":
            return interpret_var_declaration(ASTNode, env)
        case "AssignmentExpr":
            return interpret_assignment(ASTNode, env)
        case "ConditionBlock":
            return interpret_condition_block(ASTNode, env)
        case "LoopStatement":
            return interpret_loop_statement(ASTNode, env)
        case "FunctionDeclaration":
            return interpret_function_declaration(ASTNode, env)
        case "FunctionCallExpr":
            return interpret_function_call_expr(ASTNode, env)
        case "NativeFunctionCallExpr":
            return interpret_native_function_call_expr(ASTNode, env)
        case "ArrayLiteral":
            return interpret_array_declaration(ASTNode, env)
        case "ArrayAcess":
            return interpret_array_call_expr(ASTNode, env)
        case _:
            print(f"This AST Node has not been setup for interpretation yet. {ASTNode}")
            sys.exit()


# my_language/interpreter.py

def run_file(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()

        
        env = create_global_env()
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.produceAST()
        
        result = interpret(program, env)

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
