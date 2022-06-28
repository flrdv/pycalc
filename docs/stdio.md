## `print`
Semantic:
```
print(values...)
```
Returns: 0

Example:
```
print(1, 2, 3)
```
This example will print `123` WITHOUT newline in the end

---

## `println`
Semantic:
```
println(values...)
```
Returns: 0

Example:
```
println(1, 2, 3)
```
This example will print `123` WITH newline in the end

---

## `input`
Semantic:
```
input([text])
```
Returns: array with entered text in bytes

Example:
```
text = input("How are you? ")
println(text, "fine")
```
This will wait for input, after that will print back everything you typed

---

## `chr`
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

## `ord`
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
