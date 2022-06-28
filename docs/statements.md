There are no statements. But there are functions that can replace them

## `if`
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

## `branch`
Semantic:
```
branch(condition, callback[, ...[, callback]])
```
Returns: result of first true callback

Example:
```
a = 6
b = 7
branch(a == 5, ()=1, b == 7, ()=2, ()=3) == 2
```
This example will make sure that second callback will be called as b == 7 is true. In other case, the last one callback will be called

---

## `map`
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

## `reduce`
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

## `filter`
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
