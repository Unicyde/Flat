# Flat
Simple programming language to match your goals.

# *WARNING*
## *DEVELOPMENT WAS STOPPED AN THIS PROJECT (new project is Dynamo) DUE TO LARGE UGLY SOURCE CODE AND BAD PROJECT PROPOSAL YOU CAN USE THE SOURCE CODE IN YOUR PROJECTS*

## Installation

### From source
* Download the source code.
* Create file with any extenstion or just use the test.flat file.
* Launch cmd.exe/Terminal.
* Make sure that you have Python 3.x installed.
* Type `python3 path/to/source/flat.py path/to/test.someext -4`.
* The last flag/argument represents amount of spaces used for indentation.
* Enjoy some nice output or not-so-nice errors.

### From binary
* ***COMING SOON***

## About the language:
Flat is a Python-like language with dynamic type system, indentation structuring and is case-sensitive.
But it has got syntax different from all other languages:   

### Functions:
Functions can be called like that:
`function: arg1, arg2, ..., argn`
For example `print` function may be called like:   
`print: "Hello world, the magic number is ", 3.14159265`   
No more brackets.   
No more semicolons at end of line.   

But how to separate different function arguments?     
It can be done like that:   `print: "Your name is ", input: "Enter your name: "; "."`

### Taking input and variables:
Variables are declared automaticly: `myVar = "something"`    
Input is passed by showing message to user: `usrInput = input: "Enter something: "`

### If...elif...else:
The main syntax is:   
```python
if condition:  
    print: "YES"   
elif anotherCondition:   
    print: "A-bit-less YES"   
else:    
    print: "NO"
```   
You can also use advanced expressions:    
```python
if (True and True or True or False) or False:
    some code
```    
***COMING SOON***    
*I will soon implement multiple eqanations:*   
```python
if name = "John" or "Thomas" or "Paul" and surname = "Ross":
    some code
```    
