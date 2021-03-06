import enum #importing library

#creating initial variables and empty lists
operationType = 0
Exit = False
globals = {'input_token_index': -1,'next_token': '$', 'input_tokens': [], 'error':False}
symbol_table = []


class Node: #Node class converted from C Pseudo Code
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
            print("failure: unconsumed input: " +  self.unconsumed_input())
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
    #/* M ??? a | b | c | d */
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

    #/* N ??? 0 | 1 | 2 | 3 */
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
 

def lex(): #Lexical analysis function
    globals['input_token_index'] = globals['input_token_index'] + 1
    globals['next_token'] = globals['input_tokens'][globals['input_token_index']]
    if(globals['next_token'].isspace()):
        lex()

def unconsumed_input(): #function that shows the unconsumed input
    return globals['input_tokens'][globals['input_token_index']:]

def initializeParse(input_tokens): 
    globals['input_tokens'] =  input_tokens

def printTree(tree): #function to print the tree after the execution
    if(tree == None):
        return None
    else:
        printTree(tree.leftChild)
        printTree(tree.rightChild)
        print(tree.symbol)



def is_integer(n): #checking if input is integer or not
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def is_float(n): #checking if input is float or not
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


def evaluate(tree): #function to evalaute the input
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

class File: #function to take file input
    def __init__(self,file_name):
        self.file_name = file_name
        try:
            f = open(self.file_name,'r',encoding = 'utf-8')
        except OSError:
            print("No Such File: " +file_name)
    def read_input_token(self):
        f = open(self.file_name,'r',encoding = 'utf-8')
        inputs_token = f.readline()
        return inputs_token


while(not Exit): #function where everything starts
    print("1. Enter File and Run:  \n")
    print("2. Exit \n")
    operationType = int(input("Enter Operation: "))
    if(operationType == 1):
        operationFile = File(input("Enter File Name with Extension: "))
        input_tokens = operationFile.read_input_token()
        initializeParse(input_tokens)
        theTree = Node().G()
        if(globals['error'] == False):
            printTree(theTree)
            value = evaluate(theTree)
            print("The Value: " + str(value))
        else:
            print("Unsuccesful Parsing")
        print("\n")
    elif(operationType == 2):
        Exit = True

