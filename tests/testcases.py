from math import pi
from unittest import TestCase, TestSuite, makeSuite

from std.stdlibrary import stdnamespace
from pycalc.tokentypes.tokens import Function
from pycalc.interpreter.interpret import Interpreter
from pycalc.tokentypes.types import InvalidSyntaxError


interpreter = Interpreter()
evaluate = lambda code: interpreter.interpret(code, stdnamespace)


class TestNumbers(TestCase):
    def test_integer(self):
        self.assertEqual(evaluate("100"), 100)

    def test_float(self):
        self.assertEqual(evaluate("0.1"), 0.1)
        self.assertEqual(evaluate(".1"), 0.1)

    def test_hexdecimal(self):
        self.assertEqual(evaluate("0x175ffa14"), 0x175ffa14)


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

    def test_less_than(self):
        self.assertEqual(evaluate("1<2"), 1)
        self.assertEqual(evaluate("2<1"), 0)

    def test_less_equal(self):
        self.assertEqual(evaluate("2<=3"), 1)
        self.assertEqual(evaluate("2<=2"), 1)
        self.assertEqual(evaluate("2<=1"), 0)

    def test_more_than(self):
        self.assertEqual(evaluate("2>1"), 1)
        self.assertEqual(evaluate("1>2"), 0)

    def test_more_equal(self):
        self.assertEqual(evaluate("2>=1"), 1)
        self.assertEqual(evaluate("2>=2"), 1)
        self.assertEqual(evaluate("2>=3"), 0)


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
        self.assertEqual(evaluate("2**-3"), 0.125)

    def test_unary_subtraction_exponentiation(self):
        self.assertEqual(evaluate("-2**2"), -4)


class TestVariables(TestCase):
    def test_get_pi(self):
        self.assertEqual(evaluate("pi"), pi)

    def test_negotate_pi(self):
        self.assertEqual(evaluate("-pi"), -pi)

    def test_expression_with_constant(self):
        self.assertEqual(evaluate("pi+2.0-3"), pi + 2 - 3)
        self.assertEqual(evaluate("2.0+pi-3"), 2 + pi - 3)
        self.assertEqual(evaluate("2.0-3+pi"), 2 - 3 + pi)

    def test_declare_var(self):
        self.assertEqual(evaluate("a=5+5"), 10)

    def test_get_declared_var(self):
        self.assertEqual(evaluate("a=10 \n a"), 10)


class TestFunctions(TestCase):
    def test_funccall(self):
        self.assertEqual(evaluate("rt(25, 2)"), 5)

    def test_nested_funccall(self):
        self.assertEqual(evaluate("rt(rt(625, 2), 2)"), 5)

    def test_expr_in_funccall(self):
        self.assertEqual(evaluate("rt(20+5, 1.0+1.0)"), 5)

    def test_funcdef(self):
        func_a = evaluate("a()=5")
        self.assertIsInstance(func_a, Function)
        self.assertEqual(func_a.name, "a()")

        func_b = evaluate("b(x)=x+1")
        self.assertIsInstance(func_b, Function)
        self.assertEqual(func_b.name, "b(x)")

        func_c = evaluate("c(x,y)=x*y")
        self.assertIsInstance(func_c, Function)
        self.assertEqual(func_c.name, "c(x,y)")

    def test_def_func_call(self):
        self.assertEqual(evaluate("f(x,y)=x*y \n f(2,5)"), 10)

    def test_def_func_argexpr(self):
        self.assertEqual(evaluate("f(x,y)=x*y \n f(2+5, 3*2)"), 42)

    def test_funcdef_argexpr(self):
        with self.assertRaises(InvalidSyntaxError):
            evaluate("f(x+1)=x+2")

        with self.assertRaises(InvalidSyntaxError):
            evaluate("f(1)=2")

    def test_funcdef_missed_brace(self):
        with self.assertRaises(InvalidSyntaxError):
            evaluate("f(x=2")

        with self.assertRaises(InvalidSyntaxError):
            evaluate("fx)=2")

    def test_funcdef_no_body(self):
        with self.assertRaises(InvalidSyntaxError):
            evaluate("f(x)=")


class TestLambdas(TestCase):
    def test_assign_to_var(self):
        self.assertEqual(evaluate("a=(x)=x+1 \n a(1)"), 2)

    def test_lambda_as_argument(self):
        self.assertEqual(evaluate("""
        sum(mem)=reduce((x,y)=x+y, mem)
        range(begin, end) = i=begin-1; map((x)=i=i+1;x+i, malloc(end-begin))
        sum(range(0,5))
        """), 10)

    def test_missing_brace_in_arglambda(self):
        with self.assertRaises(InvalidSyntaxError):
            evaluate("sum(mem)=reduce(x,y)=x+y, mem)")

        with self.assertRaises(InvalidSyntaxError):
            evaluate("sum(mem)=reduce((x,y=x+y, mem)")

    def test_missing_brace_in_vardecl_lambda(self):
        with self.assertRaises(InvalidSyntaxError):
            evaluate("a=(x=x+1")

        with self.assertRaises(InvalidSyntaxError):
            evaluate("a=x)=x+1")


evaluation_tests = TestSuite()
evaluation_tests.addTest(makeSuite(TestNumbers))
evaluation_tests.addTest(makeSuite(TestBasicOperations))
evaluation_tests.addTest(makeSuite(TestOperatorsPriority))
evaluation_tests.addTest(makeSuite(TestVariables))
evaluation_tests.addTest(makeSuite(TestFunctions))
evaluation_tests.addTest(makeSuite(TestLambdas))
