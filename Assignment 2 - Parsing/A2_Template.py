import ply.lex as lex
import ply.yacc as yacc

# Import lexical analyzer from assignemt 1 - scanner
# import sys
# import os
# repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(os.path.join(repo_root, "Assignment 1 - Scanner"))
# import A1_MGC.py


# BEGIN LEXICAL ANALYZER DEFINITION
#
reserved = {
    # Keywords
    'if' : 'IF',           #the string (keyword) if
    'then' : 'THEN',         #the string (keyword) then
    'else' : 'ELSE',         #the string (keyword) else
    'let' : 'LET',          #the string (keyword) let
    'val' : 'VAL',          #the string (keyword) val
    'func' : 'FUNC',         #the string (keyword) func
    'end' : 'END',          #the string (keyword) end
    'in' : 'IN',           #the string (keyword) in
    'nil' : 'NIL',          #the string (keyword) nil
    'true' : 'TRUE',         #the string (keyword) true
    'false' : 'FALSE',        #the string (keyword) false
    'exec' : 'EXEC',         #the string (keyword) exec
}

tokens = [
    'IDENTIFIER',   #a string beginning with at least one lowercase or uppercase letter followed by combinations of lowercase letters, uppercase letters, digits, underscores, a single quotation, or an empty string.
    'NUMBER',       #a string consisting of one or more consecutive digits in the range 0-9
    'STRING',       #a double-quoted string. For example, “Hello”
    # Delimiters
    'LPAREN',       #the string (
    'RPAREN',       #the string )
    'LBRACE',       #the string [
    'RBRACE',       #the string ]
    'COMMA',        #the string ,
    'ASSIGN',       #the string :=

    # Operators
    'EQUAL',        #the string =
    'LESSTHAN',     #the string <
    'GREATERTHAN',  #the string >
    'PLUS',         #the string +
    'MINUS',        #the string -
    'TIMES',        #the string *
    'DIVIDE',       #the string /
    'DOT',          #the string .
    'AND',          #the string &
    'OR',           #the string |
    'UMINUS',       #Fictitous token for unanry minus
] + list(reserved.values())     # Add reserved words to token list

def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9_\']*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'[\"]([^\\\n]|(\\.))*?[\"]'
    return t

t_ignore  = ' \t\r\n'

def t_COMMENT(t):
    r'//.*'
    pass  # Ignore comment

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Define token rules for delimiters
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\['
t_RBRACE = r'\]'
t_COMMA = r','
t_ASSIGN = r':='

# Define token rules for operators
t_EQUAL = r'='
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_DOT = r'\.'
t_AND = r'&'
t_OR = r'\|'
#
# END LEXICAL ANALYZER DEFINITION

###########################

# BEGIN PARSING DEFINITION
#

# global_facts -> facts exec_line 
def p_global_facts(p):
  "global_facts : facts exec_line"
  p[0] = ("program", p[1], p[2])

# facts -> func_def facts 
#  | assign   facts 
#  | empty 
def p_facts_func(p):
  "facts : func_def"
  p[0] = [p[1]] + p[2]

def p_facts_assign(p):
  "facts : assign facts"
  p[0] = [p[1]] + p[2]

def p_facts_empty(p):
   "facts : empty"
   p[0] = []

 
# func_def -> FUNC ID_FUNC LBRACE params RBRACE ASSIGN stm END
# TO-DO

# params -> ID_FUNC COMMA params 
#  | ID COMMA params 
#  | ID_FUNC 
#  | ID
def p_params(p):
   "id"

# assign -> VAL ID ASSIGN stm END
# TO-DO

# stm -> ID_FUNC LBRACE args RBRACE
# TO-DO

# args -> ID_FUNC COMMA args 
#  | stm COMMA args 
#  | ID_FUNC 
#  | stm
# TO-DO

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
def p_stm_number(p):
  'stm : NUMBER'
  p[0] = ('number', p[1])

precedence = (
  ('left', 'PLUS', 'MINUS'),
  ('left', 'TIMES', 'DIVIDE'),
  ('right', 'UMINUS'),
)

def p_stm_binop(p):
  """stm : stm PLUS stm
        | stm MINUS stm
        | stm TIMES stm
        | stm DIVIDE stm
        | stm DOT stm 
        | stm LESSTHAN stm 
        | stm GREATERTHAN stm 
        | stm EQUAL stm 
        | stm AND stm 
        | stm OR stm"""
  p[0] = ('binop', p[2], p[1], p[3])

def p_stm_uminus(p):
  "stm : MINUS stm %prec UMINUS"
  p[0] = ('uminus', p[2])

def p_stm_string(p):
  "stm : STRING"
  p[0] = ('string', p[1])

def p_stm_bool(p):
  """stm : TRUE
        | FALSE"""
  p[0] = ('bool', p[1])
 
def p_stm_nil(p):
  "stm : NIL"
  p[0] = ('nil', p[1])

def p_stm_identifier(p):
   "stm : IDENTIFIER"
   p[0] = ("identifier", p[1])

def p_stm_group(p):
   "stm : LPAREN stm RPAREN"
   p[0] = p[2]

def p_stm_if(p):
   "stm : IF stm THEN stm ELSE stm END"
   p[0] = ('if_stm', p[2], p[4], p[6])

def p_stm_let(p):
   "stm : LET facts IN stm END"
   p[0] = ('let', p[2], p[4])
 
# exec_line -> EXEC stm
def p_exec_line(p):
   "exec_line : stm"
   p[0] = ('exec', p[2])

# empty lines
def p_empty(p):
  'empty :'
  p[0] = None

# incorrect syntax
def p_error(p):
  if p:
    print(f"Syntax error in input: {p.lineno}")
  else:
    print(f"Syntax error in input: none")
#
# END PARSING DEFINITION


# CALL PARSING 

def main():
  print("Initiating Parsing")

  # Build the lexer and parser
  lexer = lex.lex()
  parser = yacc.yacc(start='global_facts')

  # Read the file
  # textFile = open('Program_Test.txt', 'r')
  textFile = open('Assignment 2 - Parsing/Program_Test.txt', 'r')
  data = textFile.read()

  # Parse the file
  parser.parse(data, lexer=lexer)
  
  print("Finalizing Parsing")

if __name__ == '__main__':
  main()

