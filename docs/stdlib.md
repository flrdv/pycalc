## `rt`
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

## `sqrt`
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

## `cbrt`
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

## `int`
Semantic:
```
int(value[, base])
```
Returns: integer

Examples:
```
int("15") == 15
int("5f", 16)
```
First example parses a string to integer. Second does the same but for hex-decimal

---

## `float`
Semantic:
```
float(value)
```
Returns: float

Examples:
```
float("3.14") == 3.14
float("inf")
float(".5") == .5
```

---

## `str`
Semantic:
```
str(15.5)
```
Returns: string

Examples:
```
str(.5) == "0.5"
```

---

## `strjoin`
Semantic:
```
strjoin(separator, mem)
```
Returns: single string

Examples:
```
strjoin(".", "123") == "1.2.3"
```

---

## `range`
Semantic:
```
range(begin[, end[, step]])
```
Returns: array with values from `begin` to `end`. `end` is optional, if not set [0, begin) range will be returned

Example:
```
range(1, 7)
range(5)
range(2, 10, 2)
```

---

## `inv`
Semantic:
```
inv(value)
```
Returns: inverted (bitwise not) value

Example:
```
inv(5) == -6
```
