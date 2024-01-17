from batlang.bat_ast import *

# PRESIDENCE
# Conditions
# ADDITION / SUBSTRACTION
# MULTIPLICATION
# DIVISION
# PARENTHESIS


class Parser:
    def __init__(self, lexer) -> None:
        self.lexer = lexer
        self.at = lexer.get_next_token()
        self.peek_token = lexer.get_next_token()
    
    
    def not_end(self):
        return self.at.type != "EOF"


    def eat(self, token_type):
        if self.at.type == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Expected {token_type}, but got {self.at.type}")
        
    
    
    def produceAST(self):
        program = Program("Program")
        
        while(self.not_end()):
            program.body.append(self.parse_statement())
        
        return program
    
    
    def parse_statement(self):
        match self.at.type:
            case "VAR_KEYWORD":
                self.eat("VAR_KEYWORD")
                return self.parse_var_declaration()
            case "IF_KEYWORD":
                self.eat("IF_KEYWORD")
                return self.parse_condition()
            case "WHILE_KEYWORD":
                self.eat("WHILE_KEYWORD")
                return self.parse_while_statement()
            case "FUNCTION_KEYWORD":
                self.eat("FUNCTION_KEYWORD")
                return self.parse_function_declaration()
            case "ARR_KEYWORD":
                self.eat("ARR_KEYWORD")
                return self.parse_arr_declaration()
            case "COMMENT":
                self.eat("COMMENT")
            case _:
                return self.parse_expression()

    
    def parse_arr_declaration(self):
        name = self.at.value
        self.eat(self.at.type)
        self.eat("EQUALS")
        self.eat("LBRACKET")
        elements = self.parse_arr_members()
        self.eat("RBRACKET")
        
        return ArrayLiteral("ArrayLiteral", name, elements)

    
    def parse_array_call(self):
        name = self.at.value
        self.eat(self.at.type)
        self.eat("LBRACKET")
        index = self.at.value
        self.eat(self.at.type)
        self.eat("RBRACKET")
        
        return ArrayAcess("ArrayAcess", name, index)
        
        
    def parse_arr_members(self):
        elements = [self.parse_assignment_expression()]
        
        while self.at.type == "COMMA" and self.at.type != "RBRACKET":
            self.eat("COMMA")
            elements.append(self.parse_assignment_expression()) 
            
        
        return elements

    
    def parse_function_declaration(self):
        name = self.at.value
        self.eat("IDENTIFIER")
        self.eat("LPAREN")
        parameters = self.parse_parameters()
        self.eat("RPAREN")
        self.eat("LBRACE")
        
        body = []
        
        while self.at.type != "RBRACE":
            if(self.at.type == "RETURN_KEYWORD"):
                self.eat("RETURN_KEYWORD")
                body.append((self.parse_statement(), "return"))
                break
                
            body.append(self.parse_statement())
        
        self.eat("RBRACE")
        
        return FunctionDeclarationStatement("FunctionDeclaration", name, parameters, body)
    
    def peek(self):
        return self.peek_token
    
    def advance(self):
        self.at = self.peek_token
        self.peek_token = self.lexer.get_next_token()
    
    
    def parse_function_call(self):
        name = self.at.value
        self.eat("IDENTIFIER")
        self.eat("LPAREN")
        
        arguments = None
        if(self.at.type != "RPAREN"):
            arguments = self.parse_parameters()
            
        self.eat("RPAREN")
        
        return FunctionCallExpr("FunctionCallExpr", name, arguments)
    
    
    def parse_native_function_call(self):
        name = self.at.value
        self.eat(self.at.type)
        self.eat("LPAREN")
        arguments = None
        if(self.at.type != "RPAREN"):
            arguments = self.parse_parameters()
        self.eat("RPAREN")
        return NativeFunctionCallExpr("NativeFunctionCallExpr", name, arguments)
    
    
    def parse_parameters(self):
        parameters = [self.parse_assignment_expression()]
        
        while self.at.type == "COMMA" and self.at.type != "RPAREN":
            self.eat("COMMA")
            parameters.append(self.parse_assignment_expression()) 
            
        
        return parameters
        

    def parse_while_statement(self):
        conditional_expr = self.parse_conditional_expression()
        
        self.eat("LBRACE")
        while_statement = LoopStatement("LoopStatement", conditional_expr)
        
        while self.at.type != "RBRACE":
            while_statement.body.append(self.parse_statement())
        
        self.eat("RBRACE")
        
        return while_statement        


    def parse_conditional_block(self, type):
        if type != "else_block": 
            conditional_expr = self.parse_conditional_expression()
        else:
            conditional_expr = True
        
        self.eat("LBRACE")
        statements = []
        while self.at.type != "RBRACE":
            statements.append(self.parse_statement())
        self.eat("RBRACE")
        
        block = ConditionalBlock(type, conditional_expr, statements)
        
        return block

    def parse_condition(self):
        if_block = self.parse_conditional_block("if_block")
        else_block = None
        
        elif_blocks = []
        while self.at.type == "ELIF_KEYWORD":
            self.eat("ELIF_KEYWORD")
            elif_blocks.append(self.parse_conditional_block("elif_block"))
        
        if self.at.type == "ELSE_KEYWORD":
            self.eat("ELSE_KEYWORD")
            else_block = self.parse_conditional_block("else_block")         
        
        return ConditionBlock("ConditionBlock", if_block, elif_blocks, else_block)   
    
    
    def parse_var_declaration(self):
        identifier = self.at.value
        self.eat("IDENTIFIER")
        self.eat("EQUALS")
        
        declaration = VarDeclaration(type="VarDeclaration", value=self.parse_expression(), identifier=identifier)
        return declaration
    
    
    def parse_expression(self):
        return self.parse_assignment_expression()
    
    
    def parse_assignment_expression(self):
        if self.peek_token.type == "LBRACKET":
            return self.parse_array_call()
            
        left = self.parse_conditional_expression()
        
        if(self.at.type == "EQUALS"):
            self.eat("EQUALS")
            value = self.parse_assignment_expression()
            return AssignmentExpr(value=value, assigne=left, type="AssignmentExpr")

        return left
    
    def parse_conditional_expression(self):
        left = self.parse_additive_expression()
        
        while self.at.type == 'CONDITIONAL':
            condition = self.at
            self.eat(condition.type)
            
            left = ConditionalExpr(type="ConditionalExpr", left=left, right=self.parse_additive_expression(), cond=condition.value)
        
        return left
    
    def parse_additive_expression(self):
        left = self.parse_multiplicative_expression()
        
        while(self.at.value == "+" or self.at.value == "-"):
            op = self.at
            self.eat(op.type)
            
            left = BinaryExpr(type="BinaryExpr", left=left, right=self.parse_multiplicative_expression(), op=op.value)
        
        return left
    
    
    def parse_multiplicative_expression(self):
        left = self.parse_primary_expression()
        
        while(self.at.value == '/' or self.at.value == '*' or self.at.value == '%'):
            op = self.at
            self.eat(op.type)
            right = self.parse_primary_expression()
            left = BinaryExpr("BinaryExpr", left, right, op.value)
        
        return left
    
    def parse_primary_expression(self):
        token_type = self.at.type
        
        match token_type:
            case "IDENTIFIER":
                if self.peek().type == "LPAREN":
                    return self.parse_function_call()
                else:
                    identifier = Identifier("Identifier", self.at.value)
                    self.eat(token_type)
                
                return identifier
            case "NUMBER":
                expr = Numeric("Numeric", self.at.value)
                self.eat(token_type)
                return expr
            case "STRING":
                # TODO: string concatanation
                string_literal = self.at.value[1:-1]
                expr = String("String", string_literal)
                self.eat(token_type)
                return expr
            case "LPAREN":
                self.eat(token_type)
                expr = self.parse_expression()
                self.eat("RPAREN")
                return expr  
            case "INPUT_KEYWORD":
                return self.parse_native_function_call()
            case "PRINT_KEYWORD":
                return self.parse_native_function_call()
            case _:
                raise Exception(f"SyntaxError: Unexpected Character found {self.at.value}")