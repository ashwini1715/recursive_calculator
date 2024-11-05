
"""
Solutions to module 2 - A calculator
Student: Ashwini Sandeep Akula
"""

"""
Note:
The program is only working for a very tiny set of operations.
You have to add and/or modify code in ALL functions as well as add some new functions.
Use the syntax charts when you write the functions!
However, the class SyntaxError is complete as well as handling in main
of SyntaxError and TokenError.
"""

import math
from tokenize import TokenError  
from MA2tokenizer import TokenizeWrapper

class SyntaxError(Exception):
    def __init__(self, arg):
        self.arg = arg
        super().__init__(self.arg)

class EvaluationError(Exception):
    def __init__(self,message):
        self.message = message
        super().__init__(self.message)


def statement(wtok, variables):
    
    """ See syntax chart for statement"""
    result = None
    if wtok.get_current() == 'vars':
        wtok.next()
        for key, value in variables.items():
            print(f'{key}: {value}')
        wtok.next()  # Move to the next token   
    else:
        result = assignment(wtok, variables)
    if wtok.has_next():
        raise SyntaxError("Expected end of line")
        
    return result

def assignment(wtok, variables):
    """ See syntax chart for assignment"""
    result = expression(wtok,variables)
    while wtok.get_current() == '=':
        wtok.next()
        if wtok.is_name():
            variable_name = wtok.get_current()
            if variable_name in ['x','y']:
                variables[variable_name] =  result
            else:    
                variables[wtok.get_current()] = result
            wtok.next()
        else:
            raise SyntaxError("Expected variable name after '=' in assignment")
    return result

def expression(wtok, variables):
    """ See syntax chart for expression"""
    result = term(wtok, variables)
    while wtok.get_current() in ('+', '-'):
        operator = wtok.get_current()
        wtok.next()
        term_result = term(wtok,variables)
        if operator == '+':
            result += term_result
        elif operator == '-':
            result -= term_result
    return result




def term(wtok, variables):
    """ See syntax chart for term"""
    result = factor(wtok, variables)
    while wtok.get_current() in ('*' , '/') : 
        operator = wtok.get_current()
        wtok.next()
        factor_result = factor(wtok,variables)
        if operator == '*':
            result *= factor_result
        elif operator == '/':
            if factor_result == 0:
                raise EvaluationError("Division by zero")
            result /= factor_result   
    
    return result

def factorial(n):
    """Calculate the factorial of N."""
    integer_value = int(n)
    if integer_value < 0:
        raise EvaluationError(f"Argument to fac is {n}. Must be an integer.")
    else:
        return math.factorial(integer_value)


fibonacci_cache = {}

def fibonacci(n):
    if type(n) != float:
        raise EvaluationError("Decimal input is not allowed. Please provide an integer.")
    if n<0:
        raise EvaluationError(f"Argument to fib is {n}. Must be integer >=0 ")
    else:
        if n in fibonacci_cache: #Cache value first, then return it
            return fibonacci_cache[n]
    # for n sequence using memoization
        if n == 1:
            result = 1
        elif n == 2:
            result = 1
        elif n > 2:
            result = fibonacci(n-1) + fibonacci(n-2)

    fibonacci_cache[n] = result
    return result
    

def sine(n):
    """Calculate the sine of N."""
    return math.sin(n)

def cosine(n):
    """Calculate the cosine of N."""
    return math.cos(n) 

def logrithm(n):
    """Calculate the logrithm of N."""
    if n<0:
        raise EvaluationError("Arguement to log is an integer")
    else:
        return math.log(n)

def exponential(n):
    """Calculate the exponential of N."""
    return math.exp(n)


def arglist(wtok,variables):
    elements = []
    if wtok.get_current() != '(':
        raise SyntaxError("Expected '(' at the beginning of the list")
    wtok.next()
    
    while wtok.get_current() != ')' and wtok.get_current() != 'EOF':
        element= expression(wtok,variables)
        elements.append(element)

        if wtok.get_current() == ',':
            wtok.next()
        elif wtok.get_current() != ')'and wtok.get_current() != 'EOF':
            raise SyntaxError("Expected ',' or ')' next")
        
    wtok.next()
    return elements    

  
def nsum(elements):
    return sum(elements)

def nmax(elements):
    if len(elements)>0:
        return max(elements)
    else:
        raise SyntaxError("Empty list entered")


    
def nmin(elements):
    if len(elements)>0:
        return min(elements)
    else:
        raise SyntaxError("Empty list entered")
    


def nmean(elements):
    if len(elements)>0:
        return sum(elements)/len(elements)
    else:
        raise SyntaxError("Empty list entered")


function_l = {"fib": fibonacci, "fac": factorial , "sin": sine , "cos": cosine , "log": logrithm , "exp": exponential }
function_n = {"sum" : nsum ,"max" : nmax, "min" : nmin, "mean" : nmean}


def factor(wtok, variables):
    """ See syntax chart for factor"""
    if wtok.get_current() == '-':
        wtok.next()  # Move to the next token
        result = -factor(wtok, variables)      
    elif wtok.get_current() == '(':
        wtok.next()
        result = assignment(wtok, variables)
        if wtok.get_current() != ')':
            raise SyntaxError("Expected ')' after expression inside parentheses")
        wtok.next()
        return result  
    elif wtok.get_current() in function_l:
        function_name = wtok.get_current()
        wtok.next()
        if wtok.get_current() == '(':
            result = function_l[function_name](factor(wtok,variables))
        else:
            raise SyntaxError("Expected '(' after function name")
    elif wtok.get_current() in function_n:
        function_name = wtok.get_current()
        wtok.next()
        if wtok.get_current() == '(':
            result = function_n[function_name](arglist(wtok,variables))
        else:
            raise SyntaxError("Expected '(' after function name")
    elif wtok.is_name():
        variable_name = wtok.get_current()
        try:
            result = variables[variable_name]
        except KeyError:
            raise EvaluationError(f" Undefined Variable:'{variable_name}'")
        wtok.next()
    elif wtok.is_number():
        result = float(wtok.get_current())
        wtok.next()    
    else:
        raise SyntaxError("Expected number, '(' or name ")    
    return result


def main():
    """
    Handles:
       the iteration over input lines,
       commands like 'quit' and 'vars' and
       raised exceptions.
    Starts with reading the init file
    """
    
    print("Numerical calculator")
    variables = {"ans": 0.0, "E": math.e, "PI": math.pi, "x": 0.0 , "y": 0.0}
    
    

    # Note: The unit test file initiate variables in this way. If your implementation 
    # requires another initiation you have to update the test file accordingly.
    init_file = 'MA2init.txt'
    lines_from_file = ''
    try:
        with open(init_file, 'r') as file:
            lines_from_file = file.readlines()
    except FileNotFoundError:
        pass
    
    while True:
        if lines_from_file:
            line = lines_from_file.pop(0).strip()
            print('init  :', line)
        else:
            line = input('\nInput : ')
        if line == '' or line[0]=='#':
            continue
        wtok = TokenizeWrapper(line)
        if wtok.get_current() == 'quit':
            print('Bye')
            exit()
        if wtok.get_current() == 'vars':
            result = statement(wtok, variables)
            
        else:
            try:
                result = statement(wtok, variables)
                variables['ans'] = result
                print('Result:', result) 


            except SyntaxError as se:
                print("*** Syntax error: ", se)
                print(
                f"Error occurred at '{wtok.get_current()}' just after '{wtok.get_previous()}'")
            
            except TokenError as te:
                print('*** Token error: Unbalanced parentheses',te)
                print(f"Error occured at '{wtok.get_current()}' just after '{wtok.get_previous()}'")

            except EvaluationError as ee:
                print("*** Evaluation error:", ee)
                print(f"Error occured at '{wtok.get_current()}' just after '{wtok.get_previous()}'")
            


if __name__ == "__main__":
    main()
