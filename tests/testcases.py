from math import pi, sqrt
from unittest import TestCase, TestSuite, makeSuite

from pycalc.interpreter.interpret import Interpreter


interpreter = Interpreter()
basic_namespace = {
    "pi": pi,
    "sqrt": sqrt
}

evaluate = lambda code: interpreter.interpret(code, basic_namespace)


class TestNumbers(TestCase):
    def test_integer(self):
        self.assertEqual(evaluate("100"), 100)

    def test_float(self):
        self.assertEqual(evaluate("0.1"), 0.1)
        self.assertEqual(evaluate(".1"), 0.1)


class TestBasicOperations(TestCase):
    def test_addition(self):
        self.assertEqual(evaluate("1+1"), 2)

    def test_subtraction(self):
        self.assertEqual(evaluate("1-1"), 0)

    def test_multiplication(self):
        self.assertEqual(evaluate("1*1"), 1)

    def test_division(self):
        self.assertEqual(evaluate("1/2"), .5)

    def test_floordivision(self):
        self.assertEqual(evaluate("3//2"), 1)

    def test_modulo(self):
        self.assertEqual(evaluate("7%2"), 1)

    def test_lshift(self):
        self.assertEqual(evaluate("1<<5"), 32)

    def test_rshift(self):
        self.assertEqual(evaluate("128>>5"), 4)

    def test_bitwise_and(self):
        self.assertEqual(evaluate("32 & 64"), 0)

    def test_bitwise_or(self):
        self.assertEqual(evaluate("81 | 82"), 83)

    def test_bitwise_xor(self):
        self.assertEqual(evaluate("54^87"), 97)

    def test_exponentiation(self):
        self.assertEqual(evaluate("2**3"), 8)

    def test_unary_addition(self):
        self.assertEqual(evaluate("+1"), 1)

    def test_unary_subtraction(self):
        self.assertEqual(evaluate("-1"), -1)

    def test_unary_subtraction_multiple(self):
        self.assertEqual(evaluate("--1"), 1)
        self.assertEqual(evaluate("---1"), -1)

    def test_equality(self):
        self.assertEqual(evaluate("2==2"), 1)
        self.assertEqual(evaluate("2!=2"), 0)


class TestOperatorsPriority(TestCase):
    def test_addition_multiplication(self):
        self.assertEqual(evaluate("2+2*2"), 6)

    def test_addition_division(self):
        self.assertEqual(evaluate("2+2/2"), 3)

    def test_addition_exponentiation(self):
        self.assertEqual(evaluate("1+2**3"), 9)

    def test_subtraction_addition(self):
        self.assertEqual(evaluate("1-2+3"), 2)

    def test_subtraction_subtraction(self):
        self.assertEqual(evaluate("1-2-3"), -4)

    def test_subtraction_multiplication(self):
        self.assertEqual(evaluate("2-2*2"), -2)

    def test_subtraction_division(self):
        self.assertEqual(evaluate("2-2/2"), 1)

    def test_subtraction_exponentiation(self):
        self.assertEqual(evaluate("1-2**3"), -7)

    def test_multiplicaion_exponentiation(self):
        self.assertEqual(evaluate("2*10**2"), 200)

    def test_division_exponentiation(self):
        self.assertEqual(evaluate("1/10**2"), 0.01)

    def test_exponentiation_right_associativity(self):
        self.assertEqual(evaluate("2**3**2"), 512)

    def test_exponentiation_unary_subtraction(self):
        self.assertEqual(evaluate("2^-3"), 0.125)

    def test_unary_subtraction_exponentiation(self):
        self.assertEqual(evaluate("-2**2"), -4)


class TestEvaluation(TestCase):
    pass


evaluation_tests = TestSuite()
evaluation_tests.addTest(makeSuite(TestNumbers))
evaluation_tests.addTest(makeSuite(TestBasicOperations))
evaluation_tests.addTest(makeSuite(TestOperatorsPriority))
