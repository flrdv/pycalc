[![wakatime](https://wakatime.com/badge/user/b4a2ea9a-a721-41c8-b704-79b9b8cec646/project/3e68a432-deec-4dab-ba8a-a5f424e91eed.svg)](https://wakatime.com/badge/user/b4a2ea9a-a721-41c8-b704-79b9b8cec646/project/3e68a432-deec-4dab-ba8a-a5f424e91eed)
# pycalc
Simple calculator on python, written in academic purposes. TURING-COMPLETE. Uses Sorting Station Algorithm for building reverse polish notation stack. Supports all kinds of operations python supports (except bool operations like or, not, etc. but they will be implemented as a functions of std-library), functions defining, variables declarations, etc.

# How to install?
```bash
$ git clone https://github.com/fakefloordiv/pycalc && cd pycalc
```

# How to run it?
For code running, we have repl.py. It has such options:
- No options (interactive shell)
- -e, --execute: execute expression from command line
- -s, --script: execute code from file (with .calc extension)

For example:
```bash
$ python3 repl.py
```

Or:
```bash
$ python3 repl.py -e "40+2"
42
```

Even:
```bash
$ python3 repl.py -s examples/fizzbuzz.calc
```

# How to use it?
I personally allow you to use: integers, floats, constants, and functions (including defining). For example:
```
f(x,y)=x+y
40 + rt(25, 5) - pi + 0.14 / .14 << f(1,2)
```

# Documentation
See documentation in `docs/` folder.
