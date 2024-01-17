from batlang.bat_lexer import Lexer

def show_output(program):
    print("{ ")
    print(f"  kind: {program.type},")
    print("  body: [")
    for token in program.body:
        if(token.type == "Numeric"):
            show_numeric(token)
        elif(token.type == "BinaryExpr"):
            show_binary(token)
    print(" }")

def show_numeric(token):
    print("    { ")
    print(f"\tkind: {token.type},")
    print(f"\tvalue: {token.value}")
    print("    }")
    

def show_binary(token):
    print("    { ")
    print(f"\tkind: {token.type},")
    if(token.left.type == "Numeric"):
        show_numeric(token.left)
    else:
        show_binary(token.left)
    if(token.right.type == "Numeric"):
        show_numeric(token.right)
    else:
        show_binary(token.right)
    print(f"\toperator: {token.op}")
    print("    }")


def test_lexer(code):
    lexer = Lexer(code)
    while True:
        token = lexer.get_next_token()
        if token.type == "EOF":
            break
        else:
            print(f"{token.value} : {token.type}")