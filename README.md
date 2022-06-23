# pycalc
Simple calculator on python, written in academic purposes. Uses Sorting Station Algorithm for building reverse polish notation stack. Supports all kinds of operations python supports (except bool operations like or, not, etc. but they will be implemented as a functions of std-library), functions defining, variables declarations, etc.

# How to install?
```bash
$ git clone https://github.com/fakefloordiv/pycalc && cd pycalc
```

# How to run it?
```bash
$ python3 repl.py
```

This will run an interactive shell

Also, you can put an expression as an argument of command line:
```bash
$ python3 repl.py -e "40+2"
42
```

# How to use it?
I personally allow you to use: integers, floats, constants, and functions (including defining). For example:
```
f(x,y)=x+y
40 + rt(25, 5) - pi + 0.14 << f(1,2)
```

# Documentation

### Operations
There are 14 operators (and 3 internal):
- `+` add
- `-` subtract
- `/` divide
- `//` floordiv (same as usual divide, but returns integer without floating part)
- `*` multuply
- `**` power
- `%` modulo
- `<<` left bitshift
- `>>` right bitshift
- `&` bitwise and
- `|` bitwise or
- `^` bitwise xor
- `==` is equal (returns 0 if not, 1 if equal)
- `!=` not equal (inverted equal)

### Unary operations
Unary is also supported.
For example: `2+-2 == 0`
Or even: `-+--++--+-++--+++-+1 == -1`

### Numbers
Internally number is mostly float (sometimes int). There are 3 types of numbers:
- integers (example: `42`)
- floats (example: `0.42`, exponenta is not supported)
- hexdecimals (example: `0x5f3759df`)

### Variables
#### Variables declaring
To declare a variable, simply type `<name> = <value>`. 
For example: `my_constant = (0x5f3759df + 42) >> 8`

#### Get variable value
To get a value of variable, simply type its name.
For example: `my_constant + 5`

### Functions
#### Functions declaring
To define a function, simply type `<name>(<args>) = <expression>`.
For example: `f(x,y)=x+y`

Interesting fact: function body is a single expression. So this means that end of body is end of the line. So yes, currently you cannot define a function anywhere you want: usually function is a separated line

### Functions calling
To call a function, simply type `<name>(<args>)`.
For example: `root(25, 5)`

Function may have \[0, +∞) arguments, separated by comma. Function call has maximal priority (just like power)
