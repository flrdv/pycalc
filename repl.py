from typing import Optional
from sys import argv, stdin as _stdin, stdout as _stdout

from std.stdlibrary import stdnamespace
from pycalc.interpreter import interpret
from pycalc.tokentypes.types import PyCalcError, NoCodeError

PROMPT = ">> "


def _format_exc(
        code: str,
        exc: PyCalcError,
        file: str = "<anonymous>") -> str:
    lineno, pos = exc.pos
    line = code.split("\n")[lineno]

    return f"{line}\n" + \
           " " * pos + "^\n" \
           f"{file}:{lineno+1}:{pos+1}: " \
           f"{exc.__class__.__name__}: {exc}"


class InteractiveShell:
    def __init__(self,
                 prompt: str = PROMPT,
                 interpreter: Optional[interpret.ABCInterpreter] = None
                 ):
        self.prompt = prompt
        self.interpreter = interpreter or interpret.Interpreter()

    def session(self, stdin=_stdin, stdout=_stdout):
        while True:
            print(end=self.prompt, file=stdout)

            try:
                expression = stdin.readline().strip()
            except KeyboardInterrupt:
                return

            if not expression:
                continue

            try:
                print(self.interpreter.interpret(expression, stdnamespace),
                      file=stdout)
            except PyCalcError as exc:
                print(_format_exc(expression, exc, file="<repl>"),
                      file=stdout)
            except Exception as exc:
                print(f"<repl>:1:?: internal interpreter error: {exc.__class__.__name__}: {exc}",
                      file=stdout)


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
        print(_format_exc(expr, exc, file="<cli>"))
    except NoCodeError:
        pass
    except Exception as exc:
        print(f"<cli>:1:?: internal interpreter error: {exc.__class__.__name__}({repr(exc)})")


def script_exec_mode(filename: str):
    if not filename.endswith(".calc"):
        print("unsupported file extension:", filename)
        return

    try:
        with open(filename) as fd:
            code = fd.read()
    except FileNotFoundError:
        print("file not found:", filename)
        return

    interpreter = interpret.Interpreter()

    try:
        interpreter.interpret(code, stdnamespace)
    except PyCalcError as exc:
        print(_format_exc(code, exc, file=fd.name))
    except NoCodeError:
        pass
    except Exception as exc:
        print(f"{fd.name}:?:?: internal interpreter error:")
        raise exc


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
