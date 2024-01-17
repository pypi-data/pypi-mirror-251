import re


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value
        

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.keywords = {
            "batarang": "VAR_KEYWORD",
            "batIf": "IF_KEYWORD",
            "batElse": "ELSE_KEYWORD",
            "batElif": "ELIF_KEYWORD",
            "fight till": "WHILE_KEYWORD",
            "batCave": "FUNCTION_KEYWORD",
            "batSignal": "PRINT_KEYWORD",
            "batDirective": "INPUT_KEYWORD",
            "utilityBelt": "ARR_KEYWORD",
            "return": "RETURN_KEYWORD"
        }
    
    def is_keyword(self, word):
        try:
            return self.keywords[word]
        except:
            return None
        
    def get_next_token(self):
        if self.position >= len(self.source_code):
            return Token("EOF", None)

        # Define token patterns using regular expressions
        token_type = [
            (r'\d+(\.\d+)?', 'NUMBER'),  
            (r'fight till', 'LOOP'), 
            (r'\(', 'LPAREN'),            
            (r'\)', 'RPAREN'), 
            (r'\{', 'LBRACE'),
            (r'\}', 'RBRACE'),
            (r'\[', 'LBRACKET'),
            (r'\]', 'RBRACKET'),
            (r'//.*', 'COMMENT'),
            (r'\+', 'BINARY_OP'),         
            (r'-', 'BINARY_OP'),          
            (r'\*', 'BINARY_OP'),         
            (r'/', 'BINARY_OP'),          
            (r'%', 'BINARY_OP'),          
            (r'\s+', 'WHITESPACE'),       
            (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),
            (r'\<=', 'CONDITIONAL'),
            (r'\>=', 'CONDITIONAL'),
            (r'\>', 'CONDITIONAL'),
            (r'\<', 'CONDITIONAL'),
            (r'\==', 'CONDITIONAL'),
            (r'\!=', 'CONDITIONAL'),
            (r'=', 'EQUALS'),
            (r',', 'COMMA'),
            (r'(["\'])(?:(?=(\\?))\2.)*?\1', 'STRING'),
        ] 
        

        # Iterate through patterns and check for a match
        for pattern, token_type in token_type:
            regex = re.compile(pattern)
            match = regex.match(self.source_code, self.position)

            if match:
                value = match.group()
                self.position = match.end()
                if token_type == "WHITESPACE":
                    token = self.get_next_token()
                else: 
                    token = Token(token_type, value)
                
                keyword = self.is_keyword(value)
                if keyword:
                    token = Token(keyword, value)
                
                return token

        # If no pattern matches, raise an exception
        raise SyntaxError(f"Syntax Error: Invalid character '{self.source_code[self.position]}' at position {self.position}")