from interpret import interactive, interpreter

PROMPT = ">> "
CTX = {
    "rt": lambda a, b: a ** (1 / b),
    "sqrt": lambda a: a ** 1/2,
    "cbrt": lambda a: a ** 1/3,
    "pow": lambda a, b: a ** b
}


def main():
    calculator = interpreter.Calculator(ctx=CTX)
    shell = interactive.InteractiveShell(calculator)
    shell.interactive_session(prompt=PROMPT)


if __name__ == '__main__':
    main()
