import enum #importing enum Library

Exit = False #setting exit false for menu to run until we exit

#defining keywords,operators, and global variables
keyword = ["for", "while", "if", "else"]
operator = ["&&", "|", "||", "&"]
symbol_table = []
symbol_table.extend(keyword)

class Tokens(enum.Enum):#token class
    FOR = 'for'     
    WHILE = 'while'
    IF = 'if'
    ELSE = 'else'
    INTEGER = 'int'
    FLOAT = 'float'
    BITWISE_OR = '|'
    LOGICAL_OR = '||'
    BITWISE_AND = '&'
    LOGICAL_AND = '&&'
    ID = 'id'
    ERROR = 'err'

globals = {'input_token_index': -1,'next_token': '$', 'input_tokens': [], 'error':False}

class Node:
    globals = {'input_token_index': -1,'next_token': '$', 'input_tokens': [], 'error':False}
    def __init__(self, symbol='',leftChild=None, rightChild=None ):
        self.leftChild = leftChild
        self.rightChild = rightChild
        self.symbol = symbol
 
    def G(self):
        lex()
        print("G -> E")
        tree = self.E()
        if (globals['next_token'] =='$' and (not globals['error'])):
            print("success")
            return tree
        else:
            print("failure: unconsumed input: " + unconsumed_input())
            return None
    #/* E -> T R */
    def E(self):
        if (globals['error']):
            return None
        print("E -> T R")
        temp = self.T()
        return self.R(temp)
    #/* R -> + T R | - T R | e */
    def R(self, tree):
        if (globals['error']):
            return None 
        if (globals['next_token'] == '+'):
            print("R -> + T R")
            lex()
            temp1 = self.T()
            temp2 = self.R(temp1)
            x = Node('+', tree, temp2)
            return x
        elif (globals['next_token'] == '-'):
            print("R -> - T R")
            lex()
            temp1 = self.T()
            temp2 = self.R(temp1)
            x = Node('-', tree, temp2)
            return x
        else:
            print("R->e")
            return tree
    #/* T -> F S */
    def T(self):
        if (globals['error']):
            return None
        print("T -> F S")
        temp = self.F()
        return self.S(temp)
    #/* S -> * F S | / F S | e */
    def S(self, tree):
        if (globals['error']):
            return None
        if (globals['next_token']=='*'):
            print("S -> * F S")
            lex()
            temp1 = self.F()
            temp2 = self.S(temp1)
            x = Node("*", tree, temp2)
            return x
        elif (globals['next_token']=='/'):
            print("S -> / F S")
            lex()
            temp1 = self.F()
            temp2 = self.S(temp1)
            x = Node("/", tree, temp2)
            return x
        else:
            print("S -> e")
            return tree
    #/* F -> ( E ) | N */
    def F(self):
        if (globals['error']):
            return None
        if (globals['next_token']=='(' ):
            print("F->( E )")
            lex()
            temp = self.E()
            if (globals['next_token'] == ')' ):
                lex()
                return temp   
            else:
                globals['error']=True
                print("error: unexpected token " + globals['next_token']) 
                return None
        elif (globals['next_token'] in ['a' , 'b' , 'c' , 'd']):
            print("F->M")
            return self.M() 
        elif (is_integer(globals['next_token'])):
            print("F->N")
            return self.N()    
        else:
            globals['error']=True
            print("error: unexpected token " + globals['next_token'])
            return None
    #/* M  a | b | c | d */
    def M(self):
        prev_token = globals['next_token']
        if (globals['error']):
            return None
        if (globals['next_token'] in ['a' , 'b' , 'c' , 'd']):
            print("M->" + globals['next_token'])
            lex()
            x = Node(prev_token)
            return x
        else:
            globals['error']=True
            print("error: unexpected token " + globals['next_token'])
            return None

    #/* N  0 | 1 | 2 | 3 */
    def N(self):
        prev_token = globals['next_token']
        if (globals['error']):
            return None
        if (is_integer(globals['next_token'])):
            print("N->" + globals['next_token'])
            lex()
            x  = Node(prev_token)
            return x
        else :
            globals['error']=True
            print("error: unexpected token " + globals['next_token']) 
            return None    
 

def unconsumed_input():
    return globals['input_tokens'][globals['input_token_index']:]

def lex_result(input_token,  value=None): #function to return the lex result
    return value

def add_to_symbol_table(identifier): #function to add the symbols to the table
    if(symbol_table.count(identifier)):
        return symbol_table.index(identifier)
    else:
        symbol_table.append(identifier)
        return symbol_table.index(identifier)

def print_symbol_table(): #printing the symbols as table
    return "Symbol Table:  " + str(symbol_table)
    
def _lex(input_token): #lex function to identify the tokens
    if(is_operator(input_token)):
        return lex_result(input_token)
    elif(is_identifier(input_token)):
        index = add_to_symbol_table(input_token)
        return lex_result(input_token = "id", value= index)
    elif(is_keyword(input_token)):
        return lex_result(input_token)
    elif(is_integer(input_token)):
        x = int(input_token)
        return lex_result(input_token="int", value=x)
    elif(is_float(input_token)):
        x = float(input_token)
        return lex_result(input_token="float", value=x)
    else:
        return lex_result(input_token="err", value=input_token)

def lex():
    globals['input_token_index'] = globals['input_token_index'] + 1
    globals['next_token'] = globals['input_tokens'][globals['input_token_index']]
    if(globals['next_token'].isspace()):
        lex()

def initializeParse(input_tokens): #parser function
    globals['input_tokens'] =  input_tokens

def printTree(tree): #function to print the tree
    if(tree == None):
        return None
    else:
        printTree(tree.leftChild)
        printTree(tree.rightChild)
        print(tree.symbol)


def evaluate(tree): #evaluation function
    if (tree==None): 
        return -1
    if (tree.symbol == 'a'):
        return 10
    if (tree.symbol == 'b'):
        return 20
    if (tree.symbol == 'c'):
        return 30
    if (tree.symbol == 'd'):
        return 40
    if (is_integer(tree.symbol)):
        return int(tree.symbol)
    if (tree.symbol == '+'):
        return (evaluate(tree.leftChild) + evaluate(tree.rightChild))
    if (tree.symbol == '-'):
        return (evaluate(tree.leftChild) - evaluate(tree.rightChild))
    if (tree.symbol == '*'):
        return (evaluate(tree.leftChild) * evaluate(tree.rightChild))
    if (tree.symbol == '/'):
        return (evaluate(tree.leftChild) / evaluate(tree.rightChild))



def is_identifier(input_token): #function to check if the token is an identifier
    if(keyword.count(input_token)>0):
        return False
    elif(input_token[0].isalpha()):
        return True
    else:
        return False

def is_keyword(input_token): #function to check if the token is a keyword
    return bool(keyword.count(input_token))

def is_operator(input_token): #function to check if the token is an operator
    return bool(operator.count(input_token))

def is_integer(n): #function to check if the token is an integer
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def is_float(n): #function to check if the token is a float
    try:
        int_n = int(n)
    except ValueError:
        try:
            float_b = float(n)
        except ValueError:
            return False
        else:
            return True
    else:
        return False


class File: #class where we take and read the file
    def __init__(self,file_name):
        self.file_name = file_name
        try:
            f = open(self.file_name,'r',encoding = 'utf-8')
        except OSError:
            print("There is no such file: ")

    def read_input_token(self): #reading the input tokens from the file
        f = open(self.file_name,'r',encoding = 'utf-8')
        inputs_token = f.readline()
        return inputs_token


if __name__ == "__main__": #main function of the program
    while not Exit: #until we choose option 2, the function will start in this loop
        print("Parser Program is Running..." + '\n')
        print("Menu: \n")
        print("-------")
        print("1. Run the Program: ")
        print("2. Exit: ")
        instruction = int(input("Choose Your Instruction: "))
        if(instruction == 1):
            inputFile = File(input("Enter the Name of the File: "))
            input_tokens = inputFile.read_input_token()
            initializeParse(input_tokens)
            tree_Output = Node().G() #running the G function from the Node class

            if(globals['error'] == False): #if there is no error, we will get the calculated value
                printTree(tree_Output)
                value = evaluate(tree_Output)
                print("The Value: " + str(value))
            else:
                print("Unsuccessful Parsing: ")
            print("\n")
        elif(instruction == 2): #exiting the function
            print("The Program is Terminating...")
            shouldExit = True
