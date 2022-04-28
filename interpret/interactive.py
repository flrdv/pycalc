from typing import NoReturn
from sys import stdin as _stdin, stdout as _stdout

from .interpreter import Calculator


class InteractiveShell:
    exit_commands = ("quit", "exit")

    def __init__(self,
                 calculator: Calculator,
                 stdin=_stdin,
                 stdout=_stdout):
        self.calculator = calculator

        self.stdin = stdin
        self.stdout = stdout

    def _exec(self, equation: str) -> float:
        return self.calculator.execute(equation)

    def _take_input(self, prompt: str) -> str:
        self.print(prompt, end="")

        for line in self.stdin:
            return line

    def print(self, *words, end="\n", sep=" "):
        print(*words, end=end, sep=sep, file=self.stdout)

    def interactive_session(self, prompt: str = ">> ") -> NoReturn:
        while True:
            equation = self._take_input(prompt).strip()

            if equation in self.exit_commands:
                return

            try:
                result = self._exec(equation)
            except Exception as exc:
                self.print(exc.__class__.__name__, ": ", exc, sep="")
            else:
                self.print(result)
