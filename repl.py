import math
from traceback import format_exc
from typing import Optional
from sys import argv, stdin as _stdin, stdout as _stdout

from pycalc.interpreter import interpret

PROMPT = ">> "
CTX = {
    "rt": lambda a, b: a ** (1 / b),
    "sqrt": lambda a: a ** 1/2,
    "cbrt": lambda a: a ** 1/3,
    "pow": lambda a, b: a ** b,
    "pi": math.pi
}


class InteractiveShell:
    def __init__(self,
                 prompt: str = PROMPT,
                 interpreter: Optional[interpret.ABCInterpreter] = None,
                 ctx: Optional[dict] = None):
        self.prompt = prompt
        self.interpreter = interpreter or interpret.Interpreter()
        self.ctx = ctx

    def session(self, stdin=_stdin, stdout=_stdout):
        while True:
            self._print(stdout, end=self.prompt)

            try:
                expression = self._input(stdin)
            except KeyboardInterrupt:
                return

            if not expression:
                continue

            try:
                self._print(stdout, self.interpreter.interpret(expression, self.ctx))
            except Exception as exc:
                self._print(stdout, exc.__class__.__name__ + ":", exc)

    @staticmethod
    def _input(stdin) -> str:
        return stdin.readline().rstrip()

    @staticmethod
    def _print(stdout, *args, **kwargs):
        print(*args, **kwargs, file=stdout, flush=True)


def interactive_mode():
    interpreter = interpret.Interpreter()
    shell = InteractiveShell(
        prompt=PROMPT,
        interpreter=interpreter,
        ctx=CTX
    )
    shell.session()


def expr_exec_mode(expr: str):
    print(interpret.Interpreter().interpret(expr, CTX))


if __name__ == '__main__':
    if len(argv) >= 3 and argv[1] in ("-e", "--execute"):
        expr_exec_mode("".join(argv[2:]))
    else:
        interactive_mode()
