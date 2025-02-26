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
    'ID',   #a string beginning with at least one lowercase or uppercase letter followed by combinations of lowercase letters, uppercase letters, digits, underscores, a single quotation, or an empty string.
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
    'ID_FUNC',
] + list(reserved.values())     # Add reserved words to token list

def t_IDENTIFIER(t):
    r'[a-z][a-zA-Z0-9_\']*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_ID(t):
    r'[A-Z][a-zA-Z0-9_\']*'
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

# facts -> func_def facts 
#  | assign   facts 
#  | empty 
def p_facts_func(p):
  "facts : func_def"

def p_facts_assign(p):
  "facts : assign facts"

def p_facts_empty(p):
   "facts : "

# func_def -> FUNC ID_FUNC LBRACE params RBRACE ASSIGN stm END
def p_func_def(p):
   """func_def : FUNC ID_FUNC LBRACE params RBRACE ASSIGN stm END"""

# params -> ID_FUNC COMMA params 
#  | ID COMMA params 
#  | ID_FUNC 
#  | ID
def p_params(p):
   """params: ID_FUNC COMMA params 
            | ID COMMA params 
            | ID_FUNC 
            | ID"""

# assign -> VAL ID ASSIGN stm END
def p_assign(p):
   "assign : VAL ID ASSIGN stm END"
   

# stm -> ID_FUNC LBRACE args RBRACE
def p_id_func(p):
   """ID_FUNC : LBRACE args RBRACE"""

# args -> ID_FUNC COMMA args 
#  | stm COMMA args 
#  | ID_FUNC 
#  | stm
def p_args(p):
   """args : args COMMA args
           | ID_FUNC
           | stm
   """

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
precedence = (('left', 'PLUS', 'MINUS'),
              ('left', 'TIMES', 'DIVIDE'),
              ('right', 'UMINUS'),)

def p_stm_number(p):
  'stm : NUMBER'

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

def p_stm_uminus(p):
  "stm : MINUS stm %prec UMINUS"

def p_stm_string(p):
  "stm : STRING"

def p_stm_bool(p):
  """stm : TRUE
        | FALSE"""
 
def p_stm_nil(p):
  "stm : NIL"

def p_stm_identifier(p):
   "stm : ID"

def p_stm_group(p):
   "stm : LPAREN stm RPAREN"

def p_stm_if(p):
   "stm : IF stm THEN stm ELSE stm END"

def p_stm_let(p):
   "stm : LET facts IN stm END"
 
# exec_line -> EXEC stm
def p_exec_line(p):
   "exec_line : stm"

# empty lines
def p_empty(p):
  'empty :'

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

