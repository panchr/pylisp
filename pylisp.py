# Rushy Panchal
# pylisp.py
# A basic LISP interpreter, created in Python

import re

lispExtract = re.compile("\(? ?(-?(?:\w)+|\([-\w (]+\))").findall

class Expression(object):
	'''A LISP Expression'''
	def __init__(self, expression):
		self.expression = expression
		self.formatted = None
		if isinstance(expression, list):
			self.elements = expression
		else:
			self.elements = Interpreter.parse(expression)

	def evaluate(self, **values):
		'''Evaluates the LISP expression with the given values'''
		return Interpreter.interpret(self.expression, **values)

	def format(self, elements,  top = True):
		'''Formats the expression as a string'''
		if isinstance(elements, list):
			output = "'(" if top else "("
			max_index = len(elements) -1
			for index, elem in enumerate(elements):
				elemStr = self.format(elem, False) if isinstance(elem, list) else str(elem)
				output += "{leading}{item}{trailing}".format(item =  elemStr, leading = " " if index > 0 else "", trailing = "" if index == max_index else " ")
			return (output + ")").replace("  ", " ")
		else:
			return elements

	def __str__(self):
		'''Converts the expression to a string'''
		if not self.formatted:
			self.formatted = self.format(self.elements)
		return self.formatted

	def __repl__(self):
		'''Same as str(self)'''
		return str(self)

class Interpreter(object):
	'''Contains basic LISP interpretation methods'''
	spaced = " {0} ".format
	bracketed = " {0})".format

	@classmethod
	def interpret(cls, expression, **values):
		'''Interprets a given LISP expression and returns a Lisp object'''
		return cls.evaluate(cls.parse(cls.compile(expression, **values)))

	@classmethod
	def compile(cls, expression, **values):
		'''Compiles an expression with given values'''
		compiledExpr = expression
		for var, value in values.items():
			compiledExpr = compiledExpr.replace(cls.spaced(var), cls.spaced(value)).replace(cls.bracketed(var), cls.bracketed(value))
		return compiledExpr

	@classmethod
	def parse(cls, expression):
		'''Parses a given string expression and returns a Python list'''
		raw_elements = lispExtract(expression)
		recursiveExtract = lambda item: (cls.parse(item) if " " in item else item)
		return map(recursiveExtract, raw_elements)

	@classmethod
	def evaluate(cls, expressions, original = None, index = 0):
		'''Evaluate the given expressions recursively'''
		if not original:
			original = expressions
		for itemIndex, expr in enumerate(expressions):
			if isinstance(expr, list):
				cls.evaluate(expr, expressions, itemIndex)
		op = expressions[0]
		if cls.isOperator(op):
			opArgs = map(float, expressions[1:])
			opValue = OPERATIONS[expressions[0]](*opArgs)
		else:
			opValue = expressions
		original[index] = opValue
		return opValue

	@classmethod
	def isOperator(cls, op):
		'''Returns whether or not op is a valid operator'''
		return op in OPERATIONS

	@classmethod
	def register(cls, op, function):
		'''Registers a new operator'''
		OPERATIONS[op] = function

OPERATIONS = {
	"ADD": 		lambda *args: sum(args),
	"SUB": 		lambda a, b: a -b,
	"MULT": 	lambda *args: reduce(lambda a, b: a * b, args),
	"DIV": 		lambda a, b: float(a) / b,
	"EXP": 		lambda a, n: a**n,
	"SQUARE":	lambda a: a**2,
	"SQRT": 	lambda a: a**0.5,
	"CUBE": 	lambda a: a**3,
	"CUBERT":	lambda a: a**(1.0 / 3),
	"EQ": 		lambda a, b: a == b,
	"POS": 		lambda a: a > 0,
	"NEG": 		lambda a: a < 0,
	"MAX": 		lambda *args: max(args),
	"MIN": 		lambda *args: min(args),
	}
