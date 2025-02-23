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
#
#
# END PARSING DEFINITION


# CALL PARSING 

def main():
  print("Initiating Parsing")

  # Build the lexer and parser
  lexer = lex.lex()
  parser = yacc.yacc()

  # Read the file
  textFile = open('Program_Test.txt', 'r')
  data = textFile.read()

  # Parse the file
  parser.parse(data, lexer=lexer)
  
  print("Finalizing Parsing")

if __name__ == '__main__':
  main()

