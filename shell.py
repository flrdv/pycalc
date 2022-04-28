from sys import argv

from interpret import interactive, interpreter

PROMPT = ">> "
CTX = {
    "rt": lambda a, b: a ** (1 / b),
    "sqrt": lambda a: a ** 1/2,
    "cbrt": lambda a: a ** 1/3,
    "pow": lambda a, b: a ** b
}


def interactive_mode():
    calculator = interpreter.Calculator(ctx=CTX)
    shell = interactive.InteractiveShell(calculator)
    shell.interactive_session(prompt=PROMPT)


def expr_exec_mode(expr: str):
    calculator = interpreter.Calculator(ctx=CTX)
    print(calculator.execute(expr))


if __name__ == '__main__':
    if len(argv) >= 3 and argv[1] in ("-c", "--calculate"):
        expr_exec_mode("".join(argv[2:]))
    else:
        interactive_mode()
