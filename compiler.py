import sys

keywords = ("main", "def", "#def", "#int", "global", "if", "elif", "else", "while", "print", "return", "input", "int", "and", "or", "not")
separators = (":", ",")
operations = ("//", "+", "*", "-", "%")
correlations = ("<", "<=", ">", ">=", "==", "!=")
assignment = ("=")
blocks = ("(", ")", "#{", "#}")

functions = {}
variables = []
token_index = -1
tokens = []

### Classes
class Token:
    def __init__(self, recognized_token, token_type, line_number):
        self.recognized_token = recognized_token
        self.token_type = token_type
        self.line_number = line_number
    
    def __str__(self):
        return(self.recognized_token + "\t family: " + self.token_type + "\t Line: " + str(self.line_number))


### Functions

## Lexical Analyzer 
def lexicalAnalyzer(input_text):
    recognized_tokens = []
    tokens = []
    i = 0
    line_number = 1

    while i < len(input_text):
        if input_text[i] == ' ' or input_text[i] == '\t':
            # Ignore whitespaces
            i += 1
        elif input_text[i] == '\n':
            # Increment line number
            line_number += 1
            i += 1
        elif input_text[i:i+2] == '##':
            # Ignore comments
            i += 2
            while input_text[i:i+2] != '##':
                i += 1
            i += 2
        elif input_text[i:i+2] in operations:
            # Check for two-character operations
            recognized_tokens.append(('OPERATOR', input_text[i:i+2], line_number))
            i += 2
        elif input_text[i:i+2] in correlations:
            # Check for two-character correlations
            recognized_tokens.append(('CORRELATION', input_text[i:i+2], line_number))
            i += 2
        elif input_text[i:i+2] in blocks:
            # Check for two-character blocks
            recognized_tokens.append(('BLOCK', input_text[i:i+2], line_number))
            i += 2
        elif input_text[i] in operations:
            # Check for one-character operations
            recognized_tokens.append(('OPERATOR', input_text[i], line_number))
            i += 1
        elif input_text[i] in correlations:
            # Check for one-character correlations
            recognized_tokens.append(('CORRELATION', input_text[i], line_number))
            i += 1
        elif input_text[i] in blocks:
            # Check for one-character blocks
            recognized_tokens.append(('BLOCK', input_text[i], line_number))
            i += 1
        elif input_text[i] in separators:
            # Check for one-character separators
            recognized_tokens.append(('SEPARATOR', input_text[i], line_number))
            i += 1
        elif input_text[i] in assignment:
            # Check for assignment
            recognized_tokens.append(('ASSIGNMENT', input_text[i], line_number))
            i += 1
        else:
            # Identify keywords, identifiers, or integers
            token = ''
            while i < len(input_text) and input_text[i] not in (' ', '\n', '\t') and input_text[i] not in operations and input_text[i:i+2] not in operations and input_text[i] not in correlations and input_text[i:i+2] not in correlations and input_text[i:i+1] not in blocks and input_text[i] not in separators and input_text[i] not in assignment:
                token += input_text[i]
                i += 1
            if token.isdigit():
                recognized_tokens.append(('NUMBER', token, line_number))
            elif token in keywords:
                recognized_tokens.append(('KEYWORD', token, line_number))
            else:
                recognized_tokens.append(('IDENTIFIER', token, line_number))
    
    for token in recognized_tokens:
        new_token = Token(token[1], token[0], token[2])
        tokens.append(new_token)   
    return tokens

## Return next token
def nextToken():
    global token_index
    token_index += 1
    if token_index < len(tokens):
        return tokens[token_index]
    else:
        # If there are no more tokens, return a special token indicating end of file (EOF)
        return Token("EOF", "EOF", -1)

## Return previous token
def previousToken():
    global token_index
    token_index -= 1
    if token_index > -1:
        return tokens[token_index]

## Create a function that checks if the IDENTIFIER is variable or function based on functions dictionary or variables list and also the syntax of function is correct based on the value of the key in the functions dictionary
def checkIdentifier():
    global token
    global functions
    global variables
    if (token.token_type == "IDENTIFIER"):
        if (token.recognized_token in functions):
            recognized_function = token.recognized_token
            token = nextToken()
            if (token.recognized_token == "("):
                parameterCounter = 0
                token = nextToken()
                if (token.token_type == "IDENTIFIER" or token.token_type == "NUMBER"):
                    parameterCounter += 1
                    expression()
                    while (token.recognized_token == ","):
                        token = nextToken()
                        if (token.token_type == "IDENTIFIER" or token.token_type == "NUMBER"):
                            parameterCounter += 1
                            expression()
                        else:
                            print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER or NUMBER expected, but " + token.token_type + " \"" + token.recognized_token + "\" recieved.")
                            sys.exit(0)
                    if (parameterCounter == len(functions[recognized_function])):
                        if (token.recognized_token == ")"):
                            
                            token = nextToken()
                            print(token.recognized_token)
                        else:
                            print("Syntax error in line " + str(token.line_number) + ": \")\" expected, but " + token.token_type + " \"" + token.recognized_token + "\" recieved.")
                            sys.exit(0)
                    else:
                        print("Syntax error in line " + str(token.line_number) + ": The number of parameters in the function call is not correct.")
                        sys.exit(0)
                else:
                    print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " \"" + token.recognized_token + "\" recieved.")
                    sys.exit(0)
            else:
                print("Syntax error in line " + str(token.line_number) + ": \"(\" expected, but \"" + token.recognized_token + "\" recieved.")
                sys.exit(0)
        elif (token.recognized_token in keywords):
            print("Syntax error in line " + str(token.line_number) + ": The keyword \"" + token.recognized_token + "\" cannot be used as a variable.")
            sys.exit(0)
        else:
            token = nextToken()
    else:
        print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " \"" + token.recognized_token + "\" recieved.")
        sys.exit(0)

def optionalSign():
    global token
    if(token.recognized_token == "+" or token.recognized_token == "-"):
        token = nextToken()
    else:
        return
    
def parenthesis():
    global token
    if(token.recognized_token == "("):
        token = nextToken()
        expression()
        if(token.recognized_token == ")"):
            token = nextToken()
            if (token.token_type == "OPERATOR"):
                token = nextToken()
                expression()
        else:
            print("Syntax error in line " + str(token.line_number) + ": One parenthesis never closed.")
            sys.exit(0)
    else:
        print("Syntax error in line " + str(token.line_number) + ": \"(\" expected, but \"" + token.recognized_token + "\" recieved.")
        sys.exit(0)   

def expression():
    global token
    global token_index
    global code_line
    check_line = token.line_number
    optionalSign()
    if (token.token_type == "NUMBER"):
        token = nextToken()
        if (token.token_type == "OPERATOR"):
            token = nextToken()
            if (token.token_type == "NUMBER"):
                expression()
            elif (token.token_type == "IDENTIFIER"):
                checkIdentifier()
                token = previousToken()
                expression()
            elif (token.recognized_token == "("):
                parenthesis()
            else:
                print("Syntax error in line " + str(check_line) + ": Invalid expression." + token.recognized_token)
                sys.exit(0)
        elif (check_line != token.line_number or token.recognized_token in separators or token.recognized_token in correlations or token.recognized_token in keywords or token.recognized_token == ")"):
            return
        else:
            print("Syntax error in line " + str(check_line) + ": Invalid expression. " + token.recognized_token)
            sys.exit(0)
    elif (token.token_type == "IDENTIFIER"):
        checkIdentifier()
        if (token.token_type == "OPERATOR"):
            token = nextToken()
            if (token.token_type == "NUMBER"):
                expression()
            elif (token.token_type == "IDENTIFIER"):
                checkIdentifier()
                token = previousToken()
                expression()
            elif (token.recognized_token == "("):
                parenthesis()
            else:
                
                print("Syntax error in line " + str(check_line) + ": Invalid expression.1" + token.recognized_token)
                sys.exit(0)
        elif (check_line != token.line_number or token.recognized_token in separators or token.recognized_token in correlations or token.recognized_token == "and" or token.recognized_token == "or" or token.recognized_token == ")"):
            return
        else:
            print("Syntax error in line " + str(check_line) + ": Invalid expression.2" + token.recognized_token)
            sys.exit(0)
    elif (token.recognized_token == "("):
        parenthesis()
    elif (check_line != token.line_number or token.recognized_token in separators or token.recognized_token in correlations or token.recognized_token == "and" or token.recognized_token == "or" or token.recognized_token == ")"):
        return
    else:
        print("Syntax error in line " + str(token.line_number) + ": Invalid expression.3")
        sys.exit(0)

def invalidExpression(caller):
    global token
    
    if (caller == "return" or caller == "print"):
        if (token.recognized_token in separators or token.recognized_token in correlations or token.recognized_token == "and" or token.recognized_token == "or"  or token.recognized_token == ")"):
            return True
        else:
            return False
    elif (caller == "condition"):
        if(token.recognized_token in separators):
            return True
        else:
            return False
    
    

def condition():
    global token
    token = nextToken()
    expression()
    if (token.token_type == "CORRELATION"):
        token = nextToken()
        expression()
        while (token.recognized_token == "and" or token.recognized_token == "or"):
            token = nextToken()
            expression()
            if (token.token_type == "CORRELATION"):
                token = nextToken()
                expression()
            else:
                print("Syntax error in line " + str(token.line_number) + ": CORRELATION expected, but " + token.token_type + " \"" + token.recognized_token + "\" recieved.")
                sys.exit(0)
    else:
        print("DEBUG: condition()")
        print("Syntax error in line " + str(token.line_number) + ": CORRELATION expected, but " + token.token_type + " \"" + token.recognized_token + "\" recieved.")
        sys.exit(0)

## Check the syntax of elif statement
def elifStatement():
    global token
    condition()
    if (token.recognized_token == ":"):
        token = nextToken()
        if (token.recognized_token == "#{"):
            token = nextToken()
            statement()
            while (token.recognized_token != "#}"):
                if (token.token_type == "EOF"):
                    print("DEBUG: ifStatement()")
                    print("Syntax error in line " + str(token.line_number) + ": Block started but never closed.")
                    sys.exit(0)
                statement()
                token = nextToken()
        else:
            statement()
    else:
        print("Syntax error in line " + str(token.line_number) + ": SEPERATOR \":\" expected, but " + token.token_type + " " + token.recognized_token + " recieved.")
        sys.exit(0)
    if (token.recognized_token == "elif"):
        elifStatement()
    elif (token.recognized_token == "else"):
        elseStatement()

## Check the syntax of else statement   
def elseStatement():
    global token
    token = nextToken()
    if (token.recognized_token == ":"):
        token = nextToken()
        if (token.recognized_token == "#{"):
            token = nextToken()
            statement()
            while (token.recognized_token != "#}"):
                if (token.token_type == "EOF"):
                    print("DEBUG: elseStatement()")
                    print("Syntax error in line " + str(token.line_number) + ": Block started but never closed.")
                    sys.exit(0)
                statement()
                token = nextToken()
        else:
            statement()
    else:
        print("Syntax error in line " + str(token.line_number) + ": SEPERATOR \":\" expected, but " + token.token_type + " " + token.recognized_token + " recieved.")
        sys.exit(0)

## Check the syntax of if statement don't check for declarations
def ifStatement():
    global token
    condition()
    if (token.recognized_token == ":"):
        token = nextToken()
        if (token.recognized_token == "#{"):
            token = nextToken()
            statement()
            
            while (token.recognized_token != "#}"):
                if (token.token_type == "EOF"):
                    print("DEBUG: ifStatement()")
                    print("Syntax error in line " + str(token.line_number) + ": Block started but never closed.")
                    sys.exit(0)
                statement()
                token = nextToken()
        else:
            statement()
            if (token.recognized_token == "#}"):
                return
    else:
        print("Syntax error in line " + str(token.line_number) + ": SEPERATOR \":\" expected, but " + token.recognized_token + " recieved.")
        sys.exit(0)
    if (token.recognized_token == "elif"):
        elifStatement()
    elif (token.recognized_token == "else"):
        elseStatement()

## Check the syntax of while statement don't check for declarations
def whileStatement():
    global token
    token = nextToken()
    condition()
    if (token.recognized_token == ":"):
        token = nextToken()
        if (token.recognized_token == "#{"):
            token = nextToken()
            statement()
            while (token.recognized_token != "#}"):
                if (token.token_type == "EOF"):
                    print("DEBUG: whileStatement()")
                    print("Syntax error in line " + str(token.line_number) + ": Block started but never closed.")
                    sys.exit(0)
                statement()
                if (token.recognized_token != "#}"):
                    token = nextToken()
        else:
            statement()
    else:
        print("Syntax error in line " + str(token.line_number) + ": SEPERATOR \":\" expected, but " + token.token_type + " " + token.recognized_token + " recieved.")
        sys.exit(0)

def globalStatement():
    global token
    while (token.recognized_token == "global"):
        token = nextToken()
        if (token.token_type == "IDENTIFIER"):
            token = nextToken()
            while (token.recognized_token == ","):
                token = nextToken()
                if (token.token_type == "IDENTIFIER"):
                    token = nextToken()
                else:
                    print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " " + token.recognized_token + " recieved.")
                    sys.exit(0)
        else:
            print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " " + token.recognized_token + " recieved.")
            sys.exit(0)

def intStatement():
    global token
    if (token.recognized_token == "int"):
        token = nextToken()
        if (token.recognized_token == "("):
            token = nextToken()
            if (token.recognized_token == "input"):
                token = nextToken()
                if (token.recognized_token == "("):
                    token = nextToken()
                    if (token.recognized_token == ")"):
                        token = nextToken()
                        if (token.recognized_token == ")"):
                            token = nextToken()
                        else:
                            print("Syntax error in line " + str(token.line_number-1) + ": \")\" expected, but " + token.token_type + " recieved.")
                            sys.exit(0)
                    else:
                        print("Syntax error in line " + str(token.line_number-1) + ": \")\" expected, but " + token.token_type + " recieved.")
                        sys.exit(0)
                else:
                    print("Syntax error in line " + str(token.line_number) + ": \"(\" expected, but " + token.token_type + " recieved.")
                    sys.exit(0)
            else:
                print("Syntax error in line " + str(token.line_number) + ": \"input\" expected, but " + token.token_type + " recieved.")
                sys.exit(0)
        else:
            print("Syntax error in line " + str(token.line_number) + ": \"(\" expected, but " + token.recognized_token + " recieved.")
            sys.exit(0)
    else:
        print("Syntax error in line " + str(token.line_number) + ": \"int\" expected, but " + token.recognized_token + " recieved.")
        sys.exit(0)

def assignmentStatement():
    global token
    global token_index
    if (token.token_type == "IDENTIFIER"):
        token = nextToken()
        if (token.recognized_token == "="):
            token = nextToken()
            expression()
            if (token.recognized_token == "int"):
                intStatement()
            else:
                token = nextToken()
        else:
            print("Syntax error in line " + str(token.line_number) + ": Invalid syntax, \"" + token.recognized_token + "\" not expected.")
            sys.exit(0)
    else:
        print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " recieved.")
        sys.exit(0)

def returnStatement():
    global token
    check_line = token.line_number
    token = nextToken()
    if(check_line != token.line_number):
        return
    expression()
    
    if (invalidExpression("return")):
        print(token.recognized_token)
        print("hi")
        print("Syntax error in line " + str(token.line_number) + ": Invalid syntax1.")
        sys.exit(0)

def printStatement():
    global token
    check_line = token.line_number
    token = nextToken()
    if (token.recognized_token == "("):
        token = nextToken()
        expression()
        if (invalidExpression("print")):
            print("Syntax error in line " + str(token.line_number) + ": Invalid syntax2.")
            sys.exit(0)
        if (token.recognized_token == ")"):
            token = nextToken()
        else:
            print("Syntax error in line " + str(token.line_number) + ": \")\" expected, but \"" + token.recognized_token + "\" recieved.")
            sys.exit(0)
    else:
        print("Syntax error in line " + str(token.line_number) + ": \"(\" expected, but " + token.recognized_token + " recieved.")
    

def statement():
    global token
    global token_index
    token = nextToken()
    if (token.recognized_token == "="):
        token_index -= 2
        token = nextToken()
        assignmentStatement()
        token_index -= 2
        token = nextToken()
    else:
        token_index -= 2
        token = nextToken()
    if (token.recognized_token == "if"):
        ifStatement()
    elif (token.recognized_token == "while"):
        whileStatement()
    elif (token.recognized_token == "print"):
        printStatement()
        token_index -= 2
        token = nextToken()
    elif (token.recognized_token == "return"):
        returnStatement()
        token_index -= 1
        token = nextToken()
    elif (token.recognized_token == "int"):
        intStatement()

def defineVariables():
    global token
    global variables
    check_line = token.line_number
    if (token.token_type == "IDENTIFIER"):
        variables.append(token.recognized_token)
        token = nextToken()
        while (token.recognized_token == ","):
            token = nextToken()
            if (token.token_type == "IDENTIFIER"):
                variables.append(token.recognized_token)
                token = nextToken()
            else:
                print("Syntax error in line " + str(check_line) + ": IDENTIFIER expected, but " + token.token_type + " \"" + token.recognized_token + "\" recieved.")
                sys.exit(0)
    else:
        print("Syntax error in line " + str(check_line) + ": IDENTIFIER expected, but " + token.token_type + " \"" + token.recognized_token + "\" recieved.")
        sys.exit(0)
    
def declarations():
    global token
    while (token.recognized_token == "#int"):
        token = nextToken()
        defineVariables()

def subPrograms():
    global token
    global functions
    while (token.recognized_token == "def"):
        parameters = []
        token = nextToken()
        if (token.token_type == "IDENTIFIER"):
            functionName = token.recognized_token
            token = nextToken()
            if (token.recognized_token == "("):
                token = nextToken()
                if (token.token_type == "IDENTIFIER"):
                    parameters.append(token.recognized_token)
                    token = nextToken()
                    
                    while (token.recognized_token == ","):
                        token = nextToken()
                        if (token.token_type == "IDENTIFIER"):
                            parameters.append(token.recognized_token)
                            token = nextToken()
                        else:
                            print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " \"" + token.recognized_token + "\" recieved.")
                            sys.exit(0)
                if (token.recognized_token == ")"):
                    functions.update({functionName: parameters})
                    token = nextToken()
                    if (token.recognized_token == ":"):
                        token = nextToken()
                        line_number = token.line_number
                        if (token.recognized_token == "#{"):
                            token = nextToken()
                            declarations()
                            subPrograms()
                            globalStatement()
                            statement()
                            while (token.recognized_token != "#}"):
                                if (token.token_type == "EOF"):
                                    print("DEBUG: subPrograms()")
                                    print("Syntax error in line " + str(line_number) + ": Block \"#{\" started but never closed.")
                                    sys.exit(0)
                                statement()
                                token = nextToken()
                                if (token.recognized_token == "#}"):
                                    token = nextToken()
                                    return
                            else:
                                token = nextToken()
                        else:
                            print("Syntax error in line " + str(token.line_number) + ": #{ expected, but " + token.token_type + " \"" + token.recognized_token + "\" recieved.")
                            sys.exit(0)
                    else:
                        print("Syntax error in line " + str(token.line_number) + ": SEPERATOR \":\" expected, but " + token.token_type + " \"" + token.recognized_token + "\" recieved.")
                        sys.exit(0)
                else:
                    print("Syntax error in line " + str(token.line_number) + ": \")\" expected, but " + token.token_type + " \"" + token.recognized_token + "\" recieved.")
                    sys.exit(0)
            else:
                print("Syntax error in line " + str(token.line_number) + ": \"(\" expected, but " + token.token_type + " \"" + token.recognized_token + "\" recieved.")
                sys.exit(0)
        else:
            print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but \"" + token.token_type + "\" recieved.")
            sys.exit(0)

def mainProgram():
    global token
    token = nextToken()
    if (token.recognized_token == "main"):
        token = nextToken()
        declarations()
        statement()
    else:
        print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " recieved.")
        sys.exit(0)

def syntaxAnalyzer():
    global token
    global functions
    token = nextToken()
    declarations()
    subPrograms()
    if (token.recognized_token != "#def"):
        print("Syntax error in line " + str(token.line_number) + ": Unexpected token \"" + token.recognized_token + "\" recieved,You should define the main part of program.")
        sys.exit(0)
    mainProgram()
        
### Main Program
def compiler(code):
    global tokens
    tokens = lexicalAnalyzer(code)
    syntaxAnalyzer()

def main():
    if len(sys.argv) != 2:
        print("Usage: python compiler.py [filename]")
        return   

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            input_code = file.read()
            print("Start of the compilation process...")
            compiler(input_code)
            print("Compilation process completed successfully!")
    except FileNotFoundError:
        print("Error: File not found")

### Main Program
if __name__ == "__main__":
    main()