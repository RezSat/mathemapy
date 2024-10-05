import unittest
from mathemapy import *

class TestMathemapyOperations(unittest.TestCase):

    def test_addition_numbers(self):
        # Add two numbers
        num1 = Number(5)
        num2 = Number(3)
        expr = Addition(num1, num2)
        self.assertEqual(expr.evaluate(), Number(8))

    def test_addition_symbols(self):
        # Add symbols and numbers
        x = Symbol('x')
        y = Symbol('y')
        num1 = Number(5)
        num2 = Number(3)
        expr = Addition(x, Addition(y, Addition(num1, num2)))
        result = expr.evaluate()
        self.assertEqual(result, Addition(Symbol('x'), Addition(Symbol('y'), Number(8))))

    def test_subtraction(self):
        # Subtract symbols and numbers
        x = Symbol('x')
        y = Symbol('y')
        num1 = Number(5)
        num2 = Number(3)
        expr = Subtraction(x, Subtraction(y, Subtraction(num1, num2)))
        result = expr.evaluate()
        self.assertEqual(result, Subtraction(Symbol('x'), Subtraction(Symbol('y'), Number(2))))

    def test_multiplication(self):
        # Multiply numbers and symbols
        x = Symbol('x')
        y = Symbol('x')
        expr = Multiplication(x, y)
        result = expr.evaluate()
        self.assertEqual(result, Power(Symbol('x'), Number(2)))  # x * x = x^2

    def test_division(self):
        # Division of numbers
        num1 = Number(10)
        num2 = Number(2)
        expr = Division(num1, num2)
        self.assertEqual(expr.evaluate(), Number(5))

    def test_division_by_zero(self):
        # Division by zero
        num1 = Number(10)
        num2 = Number(0)
        with self.assertRaises(DivisionByZeroError):
            expr = Division(num1, num2)
            expr.evaluate()

    def test_power(self):
        # Power operation
        x = Symbol('x')
        expr = Power(x, Number(2))
        self.assertEqual(expr.evaluate(), Power(Symbol('x'), Number(2)))  # x^2

    def test_complex_addition(self):
        # Complex addition case: x + 2*x + 3 + x
        x = Symbol('x')
        y = Symbol('2x')
        num1 = Number(5)
        expr = Addition(x, Addition(y, num1))
        result = expr.evaluate()
        self.assertEqual(result, Addition(Number(5), Power(Symbol('x'), Number(3))))  # Simplified as x^3 + 5

    def test_manual_expression(self):
        x = Symbol('x')
        y = Symbol('y')
        expr1 = Addition(x, Addition(y, Number(8)))
        expr2 = Addition(x, Addition(y, Number(8)))

        self.assertEqual(expr1, expr2)

if __name__ == "__main__":
    unittest.main()
