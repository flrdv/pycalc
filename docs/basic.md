# Operations
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

# Unary operations
Unary is also supported. <br>
For example: `2+-2 == 0` <br>
Or even: `-+--++--+-++--+++-+1 == -1`

# Numbers
There are 3 types of numbers:
- integers (example: `42`)
- floats (example: `0.42`, or even `.5` (that is simply `0.5`); exponenta is not supported)
- hexdecimals (example: `0x5f3759df`, just an alternative notation of integers)

# Strings
Strings are usual strings, except only double quotes are allowed. 
`"Hello, world!"` is valid. `'Hello, world!'` is not

Strings are just strings from python. Of course, string methods aren't allowed
(just like any other methods), but all the other operations (like concatenation)
are available
