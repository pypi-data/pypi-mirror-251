import sys
from batlang.bat_values import mk_null, mk_bool

def create_global_env():
    env = Environment()
    
    
    # TODO: make a constant list where only constant value will remain
    env.declare_var("mystery", mk_null())
    env.declare_var("True", mk_bool("True"))
    env.declare_var("False", mk_bool("False"))
    
    return env
    


class Environment:
    def __init__(self, parentEnv = None) -> None:
        self.parent = parentEnv
        self.variables = dict()
    
    def declare_var(self, name, value):
        self.variables[name] = value
        return value
    
    def assign_var(self, name, value):
        env = self.resolve(name)
        
        env.variables[name] = value
        return value
        
    def lookup_var(self, name):
        env = self.resolve(name)
        return env.variables[name]

    def resolve(self, name):
        if (name in self.variables.keys()):
            return self
        
        if(self.parent == None):
            print(f"NameError: Cannot resolve '{name}' as it does not exist.")
            sys.exit()
        
        return self.parent.resolve(name)
        