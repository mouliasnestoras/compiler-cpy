from asyncio.windows_events import NULL
import sys

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
def lexicalAnalyzer():
    global code_line
    global code_file
    global eof_flag
    
    token_type = "EOF"

    current_char = ''
    next_char = code_file.read(1)
    
    ## Checking if the file is empty
    if (not next_char):
        eof_flag = True
        return (token_type, 0, code_line)

    ## Checking for white spaces
    while (next_char == ' ' or next_char == '\n' or next_char == '\t'):
        if (next_char == '\n'):
            code_line += 1

        next_char = code_file.read(1)

        if (not next_char):
            eof_flag = True
            return (token_type, "", code_line)

    ## Checking for comments or open or closed brackets
    if (next_char == '#'):
        current_char = next_char
        next_char = code_file.read(1)

        if (next_char == '#'):
            current_char = next_char
            next_char = code_file.read(1)

            start_comment = code_line
            
            current_char = next_char
            next_char = code_file.read(1)

            while (next_char != '#' or current_char != '#'):
                if (next_char == '\n'):
                    code_line += 1
        
                if (not next_char):
                    
                    print("Syntax error in line " + str(start_comment) + ": Comment section started but never closed")
                    sys.exit(0)
                    
                current_char = next_char
                next_char = code_file.read(1)
                
            return(lexicalAnalyzer())
            
        else:
            if (next_char.isalpha()):
                while (next_char.isalpha()):
                    current_char += next_char
                    next_char = code_file.read(1)
                
                code_file.seek(code_file.tell() - 1)
                
                if (current_char in keywords):
                    token_type = "KEYWORD"
                    return (token_type, current_char, code_line)
                else:
                    print("Syntax error in line " + str(code_line) + ": Not recognizing the value \"" + current_char + "\"")
                    sys.exit(0)
        
            elif (next_char == '{'):
                current_char += next_char
                token_type = "GROUP"
                return (token_type, current_char, code_line)
        
            elif (next_char == '}'):
                current_char += next_char
                token_type = "GROUP"
                return (token_type, current_char, code_line)
            
            else:
                print("Syntax error in line " + str(code_line) + ": Not recognizing the value \"" + current_char + "\"")
                sys.exit(0)
            
    ## Checking if there is identifier or keyword       
    elif (next_char.isalpha()):
        current_char = next_char
        next_char = code_file.read(1)
            
        while (next_char.isalpha() or next_char.isdigit()):
            current_char += next_char
            next_char = code_file.read(1)
        
        code_file.seek(code_file.tell() - 1)

        if (current_char in keywords):
            token_type = "KEYWORD"
            return (token_type, current_char, code_line)
        else:
            token_type = "IDENTIFIER"
            return (token_type, current_char, code_line)
        
    ## Checking for number
    elif (next_char.isdigit()):
        current_char = next_char
        next_char = code_file.read(1)

        while (next_char.isdigit()):
            current_char += next_char
            next_char = code_file.read(1)
            
        code_file.seek(code_file.tell() - 1)
        
        if (next_char.isalpha()):
            print("Syntax error in line " + str(code_line) + ": Letter \"" + next_char + "\" found after digits \"" + current_char)
            sys.exit(0)
        
        if (int(current_char) > 32767):
            print("Syntax error in line " + str(code_line) + ": The given number \"" + current_char + "\" is out of bounds, accepted numbers [-32767, 32767]")
            sys.exit(0)
        
        else:
            token_type = "NUMBER"
            return (token_type, current_char, code_line)

    ## Checking for parentheses
    elif (next_char == '(' or next_char == ')'):
        current_char = next_char
        token_type = "GROUP"
        return (token_type, current_char, code_line)
    
    ## Checking for operator
    elif (next_char == '+' or next_char == '-' or next_char == "*" or next_char == "%"):
        current_char = next_char
        token_type = "OPERATOR"
        return (token_type, current_char, code_line)
 
    ## Checking for division operator
    elif (next_char == '/'):
        current_char = next_char
        next_char = code_file.read(1)

        if (next_char == '/'):
            current_char += next_char
            token_type = "OPERATOR"
            return (token_type, current_char, code_line)
            
        else:
            print("Syntax error in line " + str(code_line) + ": Not recognizing the value \"" + current_char + "\"")
            sys.exit(0)
   
    ## Checking for seperator
    elif (next_char == ':' or next_char == ','):
        current_char = next_char
        token_type = "SEPERATOR"
        return (token_type, current_char, code_line)
    
    ## Checking for correlation or assigmnent
    elif (next_char == '='):
        current_char = next_char
        next_char = code_file.read(1)
        
        if (next_char == '='):
            current_char += next_char
            token_type = "CORRELATION"
            return (token_type, current_char, code_line)
        else:
            code_file.seek(code_file.tell() - 1)
            token_type = "ASSIGNMENT"
            return (token_type, current_char, code_line)
    
    ## Checking for number correlation
    elif (next_char == '<'):
        current_char = next_char
        next_char = code_file.read(1)
        
        if (next_char == '='):
            current_char += next_char
            token_type = "CORRELATION"
            return (token_type, current_char, code_line)
        else:
            code_file.seek(code_file.tell() - 1)
            token_type = "CORRELATION"
            return (token_type, current_char, code_line)

    ## Checking for number correlation
    elif (next_char == '>'):
        current_char = next_char
        next_char = code_file.read(1)
        
        if (next_char == '='):
            current_char += next_char
            token_type = "CORRELATION"
            return (token_type, current_char, code_line)
        else:
            code_file.seek(code_file.tell() - 1)
            token_type = "CORRELATION"
            return (token_type, current_char, code_line)

    ## Checking for number correlation
    elif (next_char == '!'):
        current_char = next_char
        next_char = code_file.read(1)
        
        if (next_char == '='):
            current_char += next_char
            token_type = "CORRELATION"
            return (token_type, current_char, code_line)
        else:
            print("Syntax error in line " + str(code_line) + ": Invalid character after the character \"" + current_char + "\"")
            sys.exit(0)

    ## Print error message if there is invalid syntax
    else:
        current_char = next_char
        print("Syntax error in line " + str(code_line) + ": Invalid syntax \"" + current_char + "\"")
        sys.exit(0)

## Return next token
def nextToken():
    global token_index
    token_index += 1
    return (tokens[token_index])

def defineVariables():
    global token
    global variables
    if (token.token_type == "IDENTIFIER"):
        variables.append(token.recognized_token)
        token = nextToken()
        while (token.recognized_token == ","):
            token = nextToken()
            if (token.token_type == "IDENTIFIER"):
                variables.append(token.recognized_token)
                token = nextToken()
            else:
                print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " " + token.recognized_token + " recieved")
                sys.exit(0)
    else:
        print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " " + token.recognized_token + " recieved")
        sys.exit(0)

## Create a function that checks if the IDENTIFIER is variable or function based on functions dictionary or variables list and also the syntax of function is correct based on the value of the key in the functions dictionary
def checkIdentifier():
    global token
    global functions
    global variables
    if (token.token_type == "IDENTIFIER"):
        if (token.recognized_token in variables):
            token = nextToken()
        elif (token.recognized_token in functions):
            token = nextToken()
            if (token.recognized_token == "("):
                parameterCounter = 0
                expression()
                token = nextToken()
                if (token.token_type == "IDENTIFIER" or token.token_type == "NUMBER"):
                    parameterCounter += 1
                    token = nextToken()
                    while (token.recognized_token == ","):
                        token = nextToken()
                        if (token.token_type == "IDENTIFIER" or token.token_type == "NUMBER"):
                            parameterCounter += 1
                            token = nextToken()
                        else:
                            print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " " + token.recognized_token + " recieved")
                            sys.exit(0)
                    if (parameterCounter == len(functions[token.recognized_token])):
                        token = nextToken()
                        if (token.recognized_token == ")"):
                            token = nextToken()
                        else:
                            print("Syntax error in line " + str(token.line_number) + ": \")\" expected, but " + token.token_type + " " + token.recognized_token + " recieved")
                            sys.exit(0)
                    else:
                        print("Syntax error in line " + str(token.line_number) + ": The number of parameters in the function call is not correct")
                        sys.exit(0)
                else:
                    print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " " + token.recognized_token + " recieved")
                    sys.exit(0)
            else:
                print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " " + token.recognized_token + " recieved")
                sys.exit(0)
        else:
            print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " " + token.recognized_token + " recieved")
            sys.exit(0)
    else:
        print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " " + token.recognized_token + " recieved")
        sys.exit(0)

def optionalSign():
    global token
    if(token.recognized_token == "+" or token.recognized_token == "-"):
        token = nextToken()
    else:
        return

def expression():
    global token
    global token_index
    optionalSign()
    if(token.token_type == "NUMBER"):
        token = nextToken()
        while(token.token_type == "OPERATOR"):
            token = nextToken()
            if(token.token_type == "NUMBER"):
                token = nextToken()
            elif(token.recognised_token == "("):
                parenthesis()
            else:
                print("Syntax error in line " + str(token.line_number) + ": Invalid expression")
                sys.exit(0)
    else:
        print("Syntax error in line " + str(token.line_number) + ": Invalid expression")
                
def parenthesis():
    global token
    if(token.recognized_token == "("):
        token = nextToken()
        expression()
        if(token.recognized_token == ")"):
            token = nextToken()
        else:
            print("Syntax error in line " + str(token.line_number) + ": \")\" expected, but " + token.token_type + " " + token.recognized_token + " recieved")
            sys.exit(0)
    else:
        print("Syntax error in line " + str(token.line_number) + ": \"(\" expected, but " + token.token_type + " " + token.recognized_token + " recieved")
        sys.exit(0)                
    
def condition():
    global token
    token = nextToken()
    expression()
    if (token.recognized_token == "CORRELATION"):
        token = nextToken()
        expression()
        while (token.recognized_token == "and" or token.recognized_token == "or"):
            token = nextToken()
            expression()
            if (token.recognized_token == "CORRELATION"):
                token = nextToken()
                expression()
            else:
                print("Syntax error in line " + str(token.line_number) + ": CORRELATION expected, but " + token.token_type + " " + token.recognized_token + " recieved")
                sys.exit(0)
    else:
        print("Syntax error in line " + str(token.line_number) + ": CORRELATION expected, but " + token.token_type + " " + token.recognized_token + " recieved")
        sys.exit(0)

    

## Check the syntax of elif statement
def elifStatement():
    global token
    token = nextToken()
    condition()
    if (token.recognized_token == ":"):
        token = nextToken()
        if (token.recognized_token == "#{"):
            token = nextToken()
            statements()
            while (token.recognized_token != "#}"):
                if (token.token_type == "EOF"):
                    print("DEBUG: elifStatement()")
                    print("Syntax error in line " + str(token.line_number) + ": Block started but never closed")
                    sys.exit(0)
                statements()
                token = nextToken()
            token = nextToken()
        else:
            print("Syntax error in line " + str(token.line_number) + ": #{ expected, but " + token.token_type + " " + token.recognized_token + " recieved")
            sys.exit(0)
    else:
        print("Syntax error in line " + str(token.line_number) + ": SEPERATOR \":\" expected, but " + token.token_type + " " + token.recognized_token + " recieved")
        sys.exit(0)
    if (token.recognized_token == "elif"):
        elifStatement()
    if (token.recognized_token == "else"):
        elseStatement()

## Check the syntax of else statement   
def elseStatement():
    global token
    token = nextToken()
    if (token.recognized_token == ":"):
        token = nextToken()
        if (token.recognized_token == "#{"):
            token = nextToken()
            statements()
            while (token.recognized_token != "#}"):
                if (token.token_type == "EOF"):
                    print("DEBUG: elseStatement()")
                    print("Syntax error in line " + str(token.line_number) + ": Block started but never closed")
                    sys.exit(0)
                statements()
                token = nextToken()
            token = nextToken()
        else:
            print("Syntax error in line " + str(token.line_number) + ": #{ expected, but " + token.token_type + " " + token.recognized_token + " recieved")
            sys.exit(0)
    else:
        print("Syntax error in line " + str(token.line_number) + ": SEPERATOR \":\" expected, but " + token.token_type + " " + token.recognized_token + " recieved")
        sys.exit(0)

## Check the syntax of if statement don't check for declarations
def ifStatement():
    global token
    token = nextToken()
    condition()
    if (token.recognized_token == ":"):
        token = nextToken()
        if (token.recognized_token == "#{"):
            token = nextToken()
            statements()
            while (token.recognized_token != "#}"):
                if (token.token_type == "EOF"):
                    print("DEBUG: ifStatement()")
                    print("Syntax error in line " + str(token.line_number) + ": Block started but never closed")
                    sys.exit(0)
                statements()
                token = nextToken()
            token = nextToken()
        else:
            expression()
    else:
        print("Syntax error in line " + str(token.line_number) + ": SEPERATOR \":\" expected, but " + token.token_type + " " + token.recognized_token + " recieved")
        sys.exit(0)
    if (token.recognized_token == "elif"):
        elifStatement()
    if (token.recognized_token == "else"):
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
            statements()
            while (token.recognized_token != "#}"):
                if (token.token_type == "EOF"):
                    print("DEBUG: whileStatement()")
                    print("Syntax error in line " + str(token.line_number) + ": Block started but never closed")
                    sys.exit(0)
                statements()
                token = nextToken()
            token = nextToken()
        else:
            print("Syntax error in line " + str(token.line_number) + ": #{ expected, but " + token.token_type + " " + token.recognized_token + " recieved")
            sys.exit(0)
    else:
        print("Syntax error in line " + str(token.line_number) + ": SEPERATOR \":\" expected, but " + token.token_type + " " + token.recognized_token + " recieved")
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
                    print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " " + token.recognized_token + " recieved")
                    sys.exit(0)
        else:
            print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " " + token.recognized_token + " recieved")
            sys.exit(0)

def intStatement():
    global token
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
                        print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " recieved")
                        sys.exit(0)
                else:
                    print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " recieved")
                    sys.exit(0)
            else:
                print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " recieved")
                sys.exit(0)
        else:
            print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " recieved")
            sys.exit(0)
    else:
        print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " recieved")
        sys.exit(0)

def assignmentStatement():
    global token
    global index
    if (token.token_type == "IDENTIFIER"):
        token = nextToken()
        if (token.recognized_token == "="):
            ## Check if the assignment value is correct with the function below
            ## assignment()
            token = nextToken()
            if (token.recognized_token == "int"):
                index -= 1
                intStatement()
            else:
                token = nextToken()
        else:
            print("Syntax error in line " + str(token.line_number) + ": Invalid syntax, \"" + token.recognized_token + "\" not expected")
            sys.exit(0)
    else:
        print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " recieved")
        sys.exit(0)

def statement():
    global token
    global token_index
    token = nextToken()
    
    if (token.recognized_token == "="):
        token_index -= 2
        token = nextToken()
        assignmentStatement()
    else:
        token_index -= 2
        token = nextToken()
    if (token.recognized_token == "if"):
        ifStatement()
    elif (token.recognized_token == "while"):
        whileStatement()
    elif (token.recognized_token == "print"):
        #printStatement()
        i = 0
    elif (token.recognized_token == "return"):
        
        returnStatement()
        
    elif (token.recognized_token == "int"):
        intStatement()

def returnStatement():
    global token
    print("hi")
    token = nextToken()
    expression()

def statements():
    token = nextToken()
    
    if(token.recognized_token == "#{"):
        block_init = token.line_number
        token = nextToken()
        statement()
        while (token.recognized_token != "#}"):
            if (token.token_type == "EOF"):
                print("DEBUG: statements()")
                print("Syntax error in line " + str(block_init) + ": Block started but never closed")
                sys.exit(0)
            statement()
            token = nextToken()
    else:
        statement()
    
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
                            print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " recieved")
                            sys.exit(0)
                if (token.recognized_token == ")"):
                    functions.update({functionName: parameters})
                    token = nextToken()
                    if (token.recognized_token == ":"):
                        token = nextToken()
                        if (token.recognized_token == "#{"):
                            token = nextToken()
                            declarations()
                            globalStatement()
                            subPrograms()
                            
                            statements()
                            while (token.recognized_token != "#}"):
                                if (token.token_type == "EOF"):
                                    print("DEBUG: subPrograms()")
                                    print("Syntax error: Block \"#{\" started but never closed")
                                    sys.exit(0)
                                statements()
                                token = nextToken()
                            token = nextToken()
                        else:
                            print("Syntax error in line " + str(token.line_number) + ": #{ expected, but " + token.token_type + " " + token.recognized_token + " recieved")
                            sys.exit(0)
                    else:
                        print("Syntax error in line " + str(token.line_number) + ": SEPERATOR \":\" expected, but " + token.token_type + " " + token.recognized_token + " recieved")
                        sys.exit(0)
            else:
                print("Syntax error in line " + str(token.line_number) + ": \"(\" expected, but " + token.token_type + " " + token.recognized_token + " recieved")
                sys.exit(0)
        else:
            print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " recieved")
            sys.exit(0)

def mainProgram():
    global token
    if (token.recognized_token == "#def"):
        token = nextToken()
        if (token.recognized_token == "main"):
            token = nextToken()
        else:
            print("Syntax error in line " + str(token.line_number) + ": IDENTIFIER expected, but " + token.token_type + " recieved")
            sys.exit(0)
    else:
        print("Syntax error in line " + str(token.line_number) + ": You should define the main part of program")
        sys.exit(0)

def program():
    # Create this function so it can recognize declaretions, functions and finally the main program of the code
    global token
    token = nextToken()
    declarations()
    subPrograms()
    #mainProgram()

## Syntax Analyzer
def syntaxAnalyzer():
    global variables
    global functions
    program()
    
        

## The main function for all processes
def startCompiling():
    while (not eof_flag):
        lexicalResult = lexicalAnalyzer()
        #print(lexicalResult)
        new_token = Token(lexicalResult[1], lexicalResult[0], lexicalResult[2])
        tokens.append(new_token)
    syntaxAnalyzer()
        
### Main Program
if __name__ == "__main__":
    functions = {}
    variables = []

    code_line = 1
    eof_flag = False
    token_index = -1
    token = ()
    tokens = []
    keywords = ("main", "def", "#def", "#int", "global", "if",
                "elif", "else", "while", "print", "return",
                "input", "int", "and", "or", "not")
    

    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()

    while lines and lines[-1].strip() == '':
        lines.pop()

    with open(sys.argv[1], 'w') as file:
        file.writelines(lines)
    
    file.close()
    
    code_file = open(sys.argv[1], "r")
    print("Start Compiling...")
    startCompiling()
    print("Compilation Completed succesfully!")
    code_file.close()