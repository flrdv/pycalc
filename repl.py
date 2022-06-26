from typing import Optional
from sys import argv, stdin as _stdin, stdout as _stdout

from std.stdlibrary import stdnamespace
from pycalc.interpreter import interpret
from pycalc.tokentypes.types import PyCalcError

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
            except PyCalcError as exc:
                self._print(stdout, expression)
                self._print(stdout, " " * exc.pos + "^")
                self._print(stdout, f"<repl>:0:{exc.pos}: {exc.__class__.__name__}: {exc}")
            except Exception as exc:
                self._print(stdout, f"<repl>:0:?: {exc.__class__.__name__}: {exc}")

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
    try:
        print(interpret.Interpreter().interpret(expr, stdnamespace))
    except PyCalcError as exc:
        print(expr)
        print(" " * exc.pos + "^")
        print(f"<cli>:0:{exc.pos}: {exc.__class__.__name__} {exc}")
    except Exception as exc:
        print(f"<cli>:0:?: {exc.__class__.__name__}: {exc}")


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
        for lineno, line in enumerate(fd, start=1):
            line = line.strip()

            if line:
                try:
                    interpreter.interpret(line, stdnamespace)
                except PyCalcError as exc:
                    print(line)
                    print(" " * exc.pos + "^")
                    print(f"{fd.name}:{lineno}:{exc.pos}: {exc.__class__.__name__}: {exc}")
                    return
                except Exception as exc:
                    print(f"{fd.name}:{lineno}:?: {exc.__class__.__name__}: {exc}")
                    return


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
    elif len(argv) == 3:
        option, value = argv[1:]
        options[option](value)
    else:
        interactive_mode()
