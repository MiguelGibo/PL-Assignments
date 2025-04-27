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

    
if __name__ == "__main__":
    # ast = {
    #     "type": "stm_value",
    #     "type_value": "number",
    #     "value": 42
    # }

    # ast = {
    #     "type": "stm_id",
    #     "id": "x"
    # }

    ast = {
        "type": "stm_op",
        "op": "+",
        "value1": {
            "type": "stm_value",
            "type_value": "number",
            "value": 3
        },
        "value2": {
            "type": "stm_value",
            "type_value": "number",
            "value": 4
        }
    }


    env = {"x": 99}

    result = interpret(ast, env=env)
    # result = interpret(parser.AST["stm"], funcs=parser.AST["facts"])
    print(result)