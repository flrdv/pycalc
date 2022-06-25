[![wakatime](https://wakatime.com/badge/user/b4a2ea9a-a721-41c8-b704-79b9b8cec646/project/3e68a432-deec-4dab-ba8a-a5f424e91eed.svg)](https://wakatime.com/badge/user/b4a2ea9a-a721-41c8-b704-79b9b8cec646/project/3e68a432-deec-4dab-ba8a-a5f424e91eed)
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
40 + rt(25, 5) - pi + 0.14 / .14 << f(1,2)
```

# Documentation

## Operations
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

## Unary operations
Unary is also supported.
For example: `2+-2 == 0`
Or even: `-+--++--+-++--+++-+1 == -1`

## Numbers
Internally number is mostly float (sometimes int). There are 3 types of numbers:
- integers (example: `42`)
- floats (example: `0.42`, or even `.5` (that is simply `0.5`); exponenta is not supported)
- hexdecimals (example: `0x5f3759df`)

## Variables
### Variables declaring
To declare a variable, simply type `<name> = <value>`. 
For example: `my_constant = (0x5f3759df + 42) >> 8`

### Get variable value
To get a value of variable, simply type its name.
For example: `my_constant + 5`

## Functions
### Functions declaring
To define a function, simply type `<name>(<args>) = <expression>`.
For example: `f(x,y)=x+y`

Interesting fact: function body is a single expression. So this means that end of body is end of the line. So yes, currently you cannot define a function anywhere you want: usually function is a separated line

### Multiple expressions in functions
Wait, what? You said function body is a single expression!
Well, yes. The problem is function body is a single expression __for interpreter__. You, as human, can write multiple expressions in function body as well. For this, you need to separate them with semicolon. Result of the last one expression is function result
For example:
```
f(x)=x+5;x
```
How do you think, what will `f(1)` return? Correct, value of `x`. `x+5` does nothing, so result of this expression will be removed from the stack after semicolon

### Higher-order functions
PyCalc supports even this. Higher-order function is a function that returns another function.
For example: 
```
f(a) = y(b) = a * b
mulBy5 = f(5)
mulBy5(5)
```
This example will return `10`

### Function calls
To call a function, simply type `<name>(<args>)`.
For example: `root(25, 5)`

Function may have \[0, +∞) arguments, separated by comma. Function call has maximal priority (just like power)

### Lambda
Lambda is simply function without name. It can be defined directly as an argument for some function. Or just be a value for some variable.

Semantic: 
```
(x, y) = x + y
```
Example: 
```
map((x)=x**2, range(0,10))
```

Or even: 
```
sqpow = (x)=x**2
sqpow(2)
```

## Standard library
### Replacing basic statements
---
#### `if`
Semantic:
```
if(condition, if[, else])
```
Returns: value returned from if or else function

Example: 
```
a = 5
if(a == 5, ()=println(chr(97)), ()=println(chr(65)))
if(a != 5, ()=println(chr(97)), ()=println(chr(65)))
```
This example prints a or A, depending on whether true or false condition is

---

#### `map`
Semantic:
```
map(func(x), mem)
```
Returns: array with new values

Example:
```
map(println, mem)
```
Here map is the same as in python. So this example will just print all the values from `mem` (that is a result of `malloc()`)

---

#### `reduce`
Semantic:
```
reduce(func(x,y), mem)
```
Returns: final value

Example:
```
reduce((x,y)=x+y, range(0,5))
```
Result of this expression is a sum of set of numbers \[0,5)

#### `filter`
Semantic:
```
filter(func(x), mem)
```
Returns: array with only values that satisfy a filter callback

Example:
```
filter((x)=x>5, range(0,10))
```
Result of this expression is array that contains ONLY numbers that are more than 5

---

### IO
#### `print`
Semantic:
```
print(values...)
```
Returns: 0

Example:
```
print(1, 2, 3)
```
This example will print `1 2 3` WITHOUT newline in the end

---

#### `println`
Semantic:
```
println(values...)
```
Returns: 0

Example:
```
println(1, 2, 3)
```
This example will print `1 2 3` WITH newline in the end

---

#### `input`
Semantic:
```
input()
```
Returns: array with entered text in bytes

Example:
```
text = input()
println(map(chr, text))
```
This will wait for input, after that will print back everything you typed

---

#### `chr`
Semantic:
```
chr(int)
```
Returns: ascii-symbol

Example:
```
println(chr(97))
```
This example will print not number 97 (as it could be without `chr()`), but `a`, that in ascii has code 97

---

#### `ord`
Semantic:
```
ord(char)
```
Returns: code of given ascii-symbol

Example:
```
ord(chr(97)) == 97
```
In this example we make sure that `a` has code 97

---

### Arrays
#### `malloc`
Semantic:
```
malloc(int)
```
Returns: array with given length filled by zeroes

Example:
```
mem = malloc(15)
println(mem)
```
This example will print an array with length of 15 filled by zeroes

---

#### `get`
Semantic:
```
get(mem, position)
```
Returns: value by given index

Example:
```
mem = range(0, 8)
get(mem, 4) == 5
```
This example will make sure that element with index 4 equals 5 (indexes are as usually, starts with 0)

---

#### `set`
Semantic:
```
set(mem, position, value)
```
Returns: 0 if everything is fine, -1 if position is out of bounds

Example:
```
mem = malloc(15)
set(mem, 0x1, 0x15)
get(mem, 0x1) == 0x15
```
This example will make sure that after we set a value 0x15 with index 1, it really equals 0x15

---

#### `sizeof`
Semantic:
```
sizeof(mem)
```
Returns: length of array

Example:
```
sizeof(malloc(15)) == 15
```
This example will make sure that newly allocated array is length of 15

---

### Other
#### `rt`
Semantic:
```
rt(value, base)
```
Returns: root of value by base

Example:
```
rt(25, 2) == 5
```

---

#### `sqrt`
Semantic:
```
sqrt(value)
```
Returns: square root of value

Example:
```
sqrt(25) == 5
```

---

#### `cbrt`
Semantic:
```
cbrt(value)
```
Returns: cube root of value

Example:
```
cbrt(9) == 3
```

---

#### `pi`
Semantic:
```
pi
```
Returns: value of pi

Example:
```
pi
```
It is actually not a function, but I'm too lazy to create a new space for constants. So here it is - constant pi
