## `malloc`
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

## `mallocfor`
Semantic:
```
mallocfor(values...)
```
Returns: memory filled with values instead of zeroes. Size of memory equals to number of given values

Example:
```
mem = mallocfor(1, 2, 3, 4, 5)
println(mem)
```
This is hello world

---

## `get`
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

## `set`
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

## `len`
Semantic:
```
len(mem)
```
Returns: length of allocated memory

Example:
```
len(malloc(15)) == 15
```
This example will make sure that newly allocated memory length is 15
