import sys

### Functions
def lexicalAnalyzer():
    global code_line
    global code_file
    global eof_flag
    
    token_type = "NONE"

    current_char = ""
    next_char = code_file.read(1)
    
    ## Checking if the file is empty
    if (not next_char):
        eof_flag = True
        return (token_type, 0, code_line)

    ## Checking for white spaces
    
    while (next_char == " " or next_char == "\n" or next_char == "\t"):
        if (next_char == "\n"):
            code_line += 1

        next_char = code_file.read(1)

        if (not next_char):
            eof_flag = True
            return (token_type, 0, code_line)

    if (next_char == "#"):
        current_char = next_char
        next_char = code_file.read(1)

        if (next_char == "#"):
            current_char = next_char
            next_char = code_file.read(1)

            start_comment = code_line
            
            current_char = next_char
            next_char = code_file.read(1)

            while (next_char != "#" or current_char != "#"):
                if (next_char == "\n"):
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
                
                if(next_char):
                    code_file.seek(code_file.tell() - 1)
                
                if (current_char in keywords):
                    token_type = "KEYWORD"
                    return (token_type, current_char, code_line)
                else:
                    print("Syntax error in line " + str(code_line) + ": Not recognizing the value \"" + current_char + "\"")
                    sys.exit(0)
        
            elif (next_char == "{"):
                current_char += next_char
                token_type = "GROUP"
                return (token_type, current_char, code_line)
        
            elif (next_char == "}"):
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
           
            next_char = code_file.read(1)
            if(not next_char.isalpha() and not next_char.isdigit()):
                if(next_char):
                    code_file.seek(code_file.tell() - 1)
                    break
            current_char += next_char
          
            ##print(next_char)
            ##print(current_char)
        if(next_char):
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
        if(next_char):    
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
            
    elif (next_char == "(" or next_char == ")"):
        current_char = next_char
        token_type = "GROUP"
        return (token_type, current_char, code_line)
    
    elif (next_char == "+" or next_char == "-" or next_char == "*" or next_char == "%"):
        current_char = next_char
        token_type = "OPERATOR"
        return (token_type, current_char, code_line)
 
    elif (next_char == "/"):
        current_char = next_char
        next_char = code_file.read(1)

        if (next_char == "/"):
            current_char += next_char
            token_type = "OPERATOR"
            return (token_type, current_char, code_line)
            
        else:
            print("Syntax error in line " + str(code_line) + ": Not recognizing the value \"" + current_char + "\"")
            sys.exit(0)
   
    elif (next_char == ":" or next_char == ","):
        current_char = next_char
        token_type = "SEPERATOR"
        return (token_type, current_char, code_line)
    
    elif (next_char == "="):
        current_char = next_char
        next_char = code_file.read(1)
        
        if (next_char == "="):
            current_char += next_char
            token_type = "CORRELATION"
            return (token_type, current_char, code_line)
        else:
            if(next_char):
                code_file.seek(code_file.tell() - 1)
            token_type = "ASSIGNMENT"
            return (token_type, current_char, code_line)
    
    elif (next_char == "<"):
        current_char = next_char
        next_char = code_file.read(1)
        
        if (next_char == "="):
            current_char += next_char
            token_type = "CORRELATION"
            return (token_type, current_char, code_line)
        else:
            if(next_char):
                code_file.seek(code_file.tell() - 1)
            token_type = "ASSIGNMENT"
            return (token_type, current_char, code_line)

    elif (next_char == ">"):
        current_char = next_char
        next_char = code_file.read(1)
        
        if (next_char == "="):
            current_char += next_char
            token_type = "CORRELATION"
            return (token_type, current_char, code_line)
        else:
            if(next_char):
                code_file.seek(code_file.tell() - 1)
            token_type = "ASSIGNMENT"
            return (token_type, current_char, code_line)
        
    elif (next_char == "!"):
        current_char = next_char
        next_char = code_file.read(1)
        
        if (next_char == "="):
            current_char += next_char
            token_type = "CORRELATION"
            return (token_type, current_char, code_line)
        else:
            print("Syntax error in line " + str(code_line) + ": Invalid character after the character \"" + current_char + "\"")
            sys.exit(0)

    else:
        current_char = next_char
        print("Syntax error in line " + str(code_line) + ": Invalid syntax \"" + current_char + "\"")
        sys.exit(0)

### The main function for all processes
def startProcessing():
    while (not eof_flag):
        print(lexicalAnalyzer())
    
### Main Program
if __name__ == "__main__":
    code_line = 1
    eof_flag = False
    
    keywords = ("main", "def", "#def", "#int", "global", "if",
                "elif", "else", "while", "print", "return",
                "input", "int", "and", "or", "not")

    code_file = open(sys.argv[1], "r")
    startProcessing()