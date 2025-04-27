import parser
def interpret(ast, env=None, funcs=None):
    if env is None:
        env = {}
    if funcs is None:
        funcs = {}
    
    type = ast['type']
    if type == 'stm_value':                                     # stm is value
        return ast['value']
    elif type == 'stm_id':                                      # stm is variable
        if ast['id'] in env:                                        # Variable exist
            return env[ast['id']]
        else:
            raise Exception(f"Undefined var: {ast['id']}")          # Variable doesn't exist
    elif type == 'stm_op':                                      # Binary operations
        val1 = interpret(ast['value1'], env=env, funcs=funcs)
        val2 = interpret(ast['value2'], env=env, funcs=funcs)
        op = ast['op']

        if op == "+":           # Sum
            return val1 + val2
        elif op == "-":         # Subtract
            return val1 - val2  
        elif op == "*":         # Multiply
            return val1 * val2 
        elif op == "/":         # Divide
            return val1 / val2
        elif op == ">":         # Greater than
            return val1 > val2
        elif op == "<":         # Less than
            return val1 < val2
        elif op == "=":         # Equal
            return val1 == val2
        elif op == "&":         # And
            return val1 and val2
        elif op == "|":         # Or
            return val1 or val2
        else:
            raise Exception(f"invalid operator {op}")
    elif type == "stm_func_call":
        if ast["id_func"] in funcs:
            func = funcs[ast['id_func']]

            evaluated_args = []
            for arg in ast['args']:
                evaluated_args.append(interpret(arg, env=env, funcs=funcs))

            params = func['params']

            if len(evaluated_args) != len(params):
                raise Exception(f"argument and parameter mismatch for {func['name']}")
            
            new_env = {}
            for i in range(len(params)):
                param_id = params[i]['id']
                new_env[param_id] = evaluated_args[i]

            return interpret(func['stm'], env=new_env, funcs=funcs)
        else:
            raise Exception(f"Undefined func {ast['id_func']}")
    elif type == "stm_let":
        facts = ast['facts']
        local_env = env.copy()

        for var_name, var_ast in facts.items():
            value = interpret(var_ast['stm'], env=env, funcs=funcs)
            local_env[var_name] = value

        return interpret(ast['stm'], env=local_env, funcs=funcs)
    elif type == "stm_if":
        condition = interpret(ast['facts'], env=env, funcs=funcs)

        if condition:
            return interpret(ast['stm_then'], env=env, funcs=funcs)
        else:
            return interpret(ast['stm_else'], env=env, funcs=funcs)
    elif type == "stm_uminus":
        value = interpret(ast['value'], env=env, funcs=funcs)
        return -value
        
# output = interpret(parser.AST["stm"], funcs=parser.AST["facts"])