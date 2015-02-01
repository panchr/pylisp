# Rushy Panchal
# pylisp.py
# A basic LISP interpreter, created in Python

import copy
import re

lispExtract = re.compile("\(? ?((?:\w)+|\([\w (]+\))").findall

class Expression(object):
	'''A LISP Expression'''
	def __init__(self, expression):
		if isinstance(expression, list):
			self.elements = expression
		else:
			self.elements = Interpreter.parse(expression)

	def evaluate(self, **values):
		'''Evaluates the LISP expression with the given values'''
		return Interpreter.evaluate(copy.deepcopy(self.elements), **values)

class Interpreter(object):
	'''Contains basic LISP interpretation methods'''
	@classmethod
	def interpret(cls, expression):
		'''Interprets a given LISP expression and returns a Lisp object'''
		return Expression(cls.parse(expression))

	@classmethod
	def parse(cls, expression):
		'''Parses a given string expression and returns a Python list'''
		raw_elements = lispExtract(expression)
		recursiveExtract = lambda item: (cls.parse(item) if " " in item else item)
		return map(recursiveExtract, raw_elements)

	@classmethod
	def evaluate(cls, expressions, original = None, index = 0, **values):
		'''Evaluate the given expressions recursively'''
		if not original:
			original = expressions
		for itemIndex, expr in enumerate(expressions):
			if isinstance(expr, list):
				cls.evaluate(expr, expressions, itemIndex, **values)
		op = expressions[0]
		if cls.isOperator(op):
			opValue = OPERATIONS[expressions[0]](expressions[1:], **values)
		else:
			opValue = expressions
		original[index] = opValue
		return opValue

	@classmethod
	def isOperator(cls, op):
		'''Returns whether or not op is a valid operator'''
		return op in VALID_OPERATIONS

def operation(function):
	'''Wrapper function to allow runtime-evaluation of LISP operations'''
	def wrapper(arguments, **values):
		arguments = map(lambda x: values[x] if isinstance(x, str) else x, arguments)
		return function(*arguments)
	return wrapper

OPERATIONS = {
	"ADD": 		operation(lambda *args: sum(args)),
	"SUB": 		operation(lambda a, b: a -b),
	"MULT": 	operation(lambda *args: reduce(lambda a, b: a * b, args)),
	"DIV": 		operation(lambda a, b: float(a) / b),
	"SQUARE":	operation(lambda a: a**2),
	"EXP": 		operation(lambda a, n: a**n),
	"EQ": 		operation(lambda a, b: a == b),
	"POS": 		operation(lambda a: a > 0),
	"NEG": 		operation(lambda a: a < 0),
	"MAX": 		operation(lambda *args: max(args)),
	"MIN": 		operation(lambda *args: min(args)),
	}

VALID_OPERATIONS = OPERATIONS.keys()
