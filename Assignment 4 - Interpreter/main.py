import scanner
import parser
import interpreter

def main():
    lexer = scanner.lexer
    par = parser.parser

    with open("Program_Test1.txt", "r") as f:
        data = f.read()

    ast = par.parse(data, lexer=lexer)
    result = interpreter.interpret(ast['stm'], funcs=ast['facts'])

    print(result)

if __name__ == "__main__":
    main()