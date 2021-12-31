'''
File containing the environment class.

'''


class Environment:
    
    
    def __init__(self):
        self.values = dict()
        
        
    def define(self, name, value):
        ''' Function to define a new environment variable. '''
        self.values[name] = value
        
        
    def get(self, name):
        ''' Function to get an environment variable. '''
        if name in self.values:
            return self.values[name]
        else:
            raise RuntimeError(f'Undefined variable "{name.lexeme}"')
            
            
    def assign(self, name, value):
        '''
        Function to assign a variable a value. 
        
        Similar to define() but cannot assign a new variable.
        
        '''
        key = name.lexeme
        if key in self.values:
            self.values[key] = value
        else:
            raise RuntimeError(f'Undefined variable "{key}"')
        
        
        

