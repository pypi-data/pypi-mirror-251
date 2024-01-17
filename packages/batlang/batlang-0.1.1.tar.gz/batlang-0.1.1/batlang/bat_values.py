class RuntimeVal:
    def __init__(self, type) -> None:
        self.type = type


class NullVal(RuntimeVal):
    def __init__(self, type) -> None:
        self.value = "mystery"
        super().__init__(type)

def mk_null():
    return NullVal("null")


class BooleanVal(RuntimeVal):
    def __init__(self, type, value) -> None:
        self.value = value
        super().__init__(type)        

def mk_bool(b):
    return BooleanVal("boolean", b)

    
class NumberVal(RuntimeVal):
    def __init__(self, type, value):
        self.value = value
        super().__init__(type)


class ConditionalVal(RuntimeVal):
    def __init__(self, type, value) -> None:
        self.value = value
        super().__init__(type)


class StringVal(RuntimeVal):
    def __init__(self, type, value) -> None:
        self.value = value
        super().__init__(type)



class NativeFnVal(RuntimeVal):
    def __init__(self, type, call) -> None:
        self.type = type
        self.call = call
        super().__init__(type)



class FunctionValue(RuntimeVal):
    def __init__(self, type, name, parameters, env, body) -> None:
        self.name = name
        self.parameters = parameters
        self.env = env
        self.body = body
        super().__init__(type)


class ArrayLiteralValue(RuntimeVal):
    def __init__(self, type, name, elements) -> None:
        self.name = name
        self.value = elements
        super().__init__(type)


class ArrayMember(RuntimeVal):
    def __init__(self, type, value) -> None:
        self.value = value
        super().__init__(type)