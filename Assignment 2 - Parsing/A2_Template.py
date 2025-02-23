import ply.lex as lex
import ply.yacc as yacc

# Import lexical analyzer from assignemt 1 - scanner
import sys
import os
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(repo_root, "Assignment 1 - Scanner"))
import A1_MGC.py


# BEGIN LEXICAL ANALYZER DEFINITION
#
#
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

