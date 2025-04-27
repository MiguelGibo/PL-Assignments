import ply.yacc as yacc
import scanner
import json
tokens = scanner.tokens

# BEGIN PARSING DEFINITION
#

# global_facts -> facts exec_line 
def p_global_facts(p):
  "global_facts : facts exec_line" 
  p[0] = {"facts": p[1],
          "stm": p[2]}

# facts -> func_def facts 
#  | assign   facts 
#  | empty 
def p_facts_func(p):
  "facts : func_def facts"
  p[0] = {**p[1], **p[2]}

def p_facts_assign(p):
  "facts : assign facts"
  p[0] = {**p[1], **p[2]}

def p_facts_empty(p):
   "facts :"
   p[0] = {}

# func_def -> FUNC ID_FUNC LBRACE params RBRACE ASSIGN stm END
def p_func_def(p):
   "func_def : FUNC ID_FUNC LBRACE params RBRACE ASSIGN stm END"
   p[0] = {p[2]: {"type":'func',
                  "name": p[2],
                  "params": p[4],
                  "stm": p[7]}}

# params -> ID_FUNC COMMA params 
#  | ID COMMA params 
#  | ID_FUNC 
#  | ID
def p_params_func(p):
   """
   params : ID_FUNC COMMA params 
          | ID COMMA params
   """
   p[0] = [{"type":'id',
            'id':p[1]}] + p[3]
   
def p_params_ID(p):
   """
   params : ID_FUNC 
          | ID
   """
   p[0] = [{"type":'id',
            'id':p[1]}]

# assign -> VAL ID ASSIGN stm END
def p_assign(p):
   "assign : VAL ID ASSIGN stm END"
   p[0] = {p[2]: {"type": "val",
                  "name": p[2],
                  "stm": p[4]}}
   

# stm -> ID_FUNC LBRACE args RBRACE
def p_id_func(p):
   "stm : ID_FUNC LBRACE args RBRACE"
   p[0] = {"type": "stm_func_call",
           "id_func": p[1],
           "args": p[3]}


# args -> ID_FUNC COMMA args 
#  | stm COMMA args 
#  | ID_FUNC 
#  | stm
def p_args(p):
   """
   args : ID_FUNC COMMA args
        | stm COMMA args
        | ID_FUNC
        | stm
   """
   if len(p) == 2:
      p[0] = [p[1]]
   else:
      p[0] = [p[1]] + p[3]

# stm -> stm PLUS stm  
#  |stm MINUS stm 
#  | stm TIMES stm 
#  | stm DIVIDE stm 
#  | stm DOT stm 
#  | stm LESSTHAN stm 
#  | stm GREATERTHAN stm 
#  | stm EQUAL stm 
#  | stm AND stm 
#  | stm OR stm 
#  |STRING 
#  |NUMBER 
#  |TRUE 
#  |FALSE 
#  |NIL 
#  |ID 
#  |LPAREN stm RPAREN 
#  |IF stm THEN stm ELSE stm END 
#  |LET facts IN stm END 
precedence = (
   ('left', 'OR', 'AND'),
   ('nonassoc', 'EQUAL', 'LESSTHAN', 'GREATERTHAN'),
   ('left', 'PLUS', 'MINUS'),
   ('left', 'TIMES', 'DIVIDE'),
   ('right', 'UMINUS'),
   ('left', 'LBRACE', 'RBRACE'),)

def p_stm_binop(p):
   """
   stm  : stm PLUS stm
        | stm MINUS stm
        | stm TIMES stm
        | stm DIVIDE stm
        | stm DOT stm 
        | stm LESSTHAN stm 
        | stm GREATERTHAN stm 
        | stm EQUAL stm 
        | stm AND stm 
        | stm OR stm
   """
   p[0] = {"type": "stm_op",
           "op": p[2],
           "value1": p[1],
           'value2': p[3]}
   
def p_stm_string(p):
  "stm : STRING"
  p[0] = {'type': "stm_value",
          'type_value': "string",
          'value': p[1]}

def p_stm_number(p):
  'stm : NUMBER'
  p[0] = {'type': "stm_value",
          'type_value': "number",
          'value': p[1]}

def p_stm_bool(p):
  """
  stm : TRUE
      | FALSE
  """
  p[0] = {'type': "stm_value",
          'type_value': "bool",
          'value': p[1]}
 
def p_stm_nil(p):
  "stm : NIL"
  p[0] = {'type': "stm_value",
          'type_value': "nil",
          'value': None}

def p_stm_id(p):
   "stm : ID"
   p[0] = {'type':'stm_id',
           'id': p[1]}

def p_stm_group(p):
   "stm : LPAREN stm RPAREN"
   p[0] = p[2]

def p_stm_if(p):
   "stm : IF stm THEN stm ELSE stm END"
   p[0] = {'type': "stm_if",
           'facts': p[2],
           'stm':p[4]}

def p_stm_let(p):
   "stm : LET facts IN stm END"
   p[0] = {'type': 'stm_let',
           'facts':p[2],
           'stm':p[4]}

def p_stm_uminus(p):
  "stm : MINUS stm %prec UMINUS"
  p[0] = {'type': "stm_uminus",
          "value": p[2]}
 
# exec_line -> EXEC stm
def p_exec_line(p):
   "exec_line : EXEC stm"
   p[0] = p[2]

# empty lines
def p_empty(p):
  'empty :'
  pass

# incorrect syntax
def p_error(p):
  if p:
    print(f"Syntax error in input: {p.lineno}")
  else:
    print("Syntax error in input: none")
#
# END PARSING DEFINITION


# CALL PARSING 
parser = yacc.yacc(start='global_facts')


textFile = open('Program_Test2.txt', 'r')
data = textFile.read()
AST = parser.parse(data, lexer=scanner.lexer)
# print(json.dumps(AST, indent=2))