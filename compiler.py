import sys

### Functions
def lexicalAnalyzer():
    global code_line
    global code_index
    
    return (0, 0, 0)


def startProcessing():
    lexicalAnalyzer()
    
### Main Program

if __name__ == "__main__":
    code_line = 0
    code_index = 0
    
    keywords = ("main", "def", "#def", "#int", "global", "if",
                "elif", "else", "while", "print", "return",
                "input", "int", "and", "or", "not")

    code_file = open(sys.argv[1], "r")
    startProcessing()
    