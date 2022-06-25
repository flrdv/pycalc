from typing import Optional
from sys import argv, stdin as _stdin, stdout as _stdout

from pycalc.interpreter import interpret
from std.stdlibrary import stdnamespace

PROMPT = ">> "


class InteractiveShell:
    def __init__(self,
                 prompt: str = PROMPT,
                 interpreter: Optional[interpret.ABCInterpreter] = None
                 ):
        self.prompt = prompt
        self.interpreter = interpreter or interpret.Interpreter()

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
                self._print(stdout, self.interpreter.interpret(expression, stdnamespace))
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
        interpreter=interpreter
    )
    shell.session()


def expr_exec_mode(expr: str):
    print(interpret.Interpreter().interpret(expr, stdnamespace))


def script_exec_mode(filename: str):
    if not filename.endswith(".calc"):
        print("unsupported file extension:", filename)
        return

    try:
        fd = open(filename)
    except FileNotFoundError:
        print("file not found:", filename)
        return

    interpreter = interpret.Interpreter()

    with fd:
        for line in fd:
            interpreter.interpret(line, stdnamespace)


if __name__ == '__main__':
    options = {
        "-e":        expr_exec_mode,
        "--execute": expr_exec_mode,
        "-s":       script_exec_mode,
        "--script": script_exec_mode,
    }

    if len(argv) > 1 and (argv[1] not in options or len(argv) != 3):
        print("Invalid options:", " ".join(argv[1:]))
        print("Available options:")
        print("\t-e, --execute <expression>: execute expression right from a command line")
        print("\t-s, --script <filename>.calc: execute program from a file")
    if len(argv) == 3:
        option, value = argv[1:]
        options[option](value)
    else:
        interactive_mode()
