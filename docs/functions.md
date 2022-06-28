## Functions
### Functions declaring
To define a function, simply type `<name>(<args>) = <expression>`.
For example: `f(x,y)=x+y`

Also, multi-lined functions are allowed. Rules of expression lines break:
- Expression is inside of parenthesis
- Or there is an operator in the end of previous line

For example:
```
f(x, y) = 
    a = x + y;
    println(a)
```

Or:

```
sum(mem) = reduce(
    (x, y) = x + y,
    mem
)
```

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
This example will return `25`

### Function calls
To call a function, simply type `<name>(<args>)`.
For example: `root(25, 2)`

Function may have \[0, +∞) arguments, separated by comma. Function call has maximal priority (just like power)

### Lambda
Lambda is simply function without name. It can be defined directly as an argument for some function. Or just be a value for some variable.

Semantic: 
```
(x, y) = x + y
```
Example: 
```
map((x)=x**2, range(0, 10))
```

Or even: 
```
sqpow = (x)=x**2
sqpow(2)
```