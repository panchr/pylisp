# pylisp
A small, minimalist LISP interpreter written in Python

This is a proof-of-concept work. As such, there will not be any stable releases.

## Features
Currently, `pylisp` only supports basic numeric LISP. It works with any of the [listed operations](#operators).
In addition, it supports arbitrarily nested lists.
Finally, you can register new operators, mapping a name to a Python function.

## Usage
All of the usage examples assume that `pylisp` has been imported: `import pylisp`.
The easiest way to use `pylisp` is with the `Expression` class. Simply pass a valid LISP expression (as a string) and it will be automatically parsed. Currently, `pylisp` does not check for validity, so an invalid expression will break things.

Let's start simple, with the LISP expression of `(ADD 2 3)`:
```python
expr = pylisp.Expression("(ADD 2 3)")
print expr.evaluate() # --> 5.0
```
First, we create an expression by using the `Expression` class. Then, we evaluate it with the `.evaluate` method.

We can also have nested expressions:
```python
expr = pylisp.Expression("(ADD 2 (MULT 5 3))")
print expr.evaluate() # --> 17.0
```

Finally, we can use variables instead of numeric literals:
```python
expr = pylisp.Expression("(ADD 2 (MULT A B) C)")
print expr.evaluate(A = 2, B = 5, C = 1) # --> 13
```

## Operators
There are a few standard LISP operators as well as a few custom operators that come included.

|Operator|Arguments|Mathematical equivalent
---------|---------|-----------
|SUM|a, b, c, ...|Sum of {a, b, c, ...}|
|SUB|a, b|a - b|
|MULT|a, b, c, ...|Product of {a, b, c, ...}|
|DIV|a, b|a / b|
|EXP|a, b|a<sup<b</sup>|
|SQUARE|a|a<sup>2</sup>|
|SQRT|a|a<sup>0.5</sup>|
|CUBE|a|a<sup>3</sup>|
|CUBERT|a|a<sup>1/3</sup>|
|EQ|a, b|a == b
|POS|a|a > 0
|NEG|a|a < 0
|MAX|a, b, c, ...|Maximum value of {a, b, c, ...}
|MIN|a, b, c, ...|Minimum value of {a, b, c, ...}

New operators can be registered using the `Interpreter.register` method:
```python
def neq(a, b):
  return a != b
  
Interpreter.register("NEQ", neq)
Interpreter.register("GE", lambda a, b: a > b)
```

As shown, the `.register` method takes an operation name (a string) and an operator function. The function should accept numeric values and return a numeric (or Boolean) value.
