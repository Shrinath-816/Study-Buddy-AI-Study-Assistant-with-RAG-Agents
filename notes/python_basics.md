# Python Basics - Programming Notes

## Variables and data types
A variable is a name that stores a value, e.g. `age = 16`. Python works out the type automatically.
Common data types:
- `int` - whole numbers, e.g. 42
- `float` - decimal numbers, e.g. 3.14
- `str` - text (strings), written in quotes, e.g. "hello"
- `bool` - True or False

## Lists
A list stores many items in order, inside square brackets: `fruits = ["apple", "banana", "cherry"]`.
- Lists are **mutable**: you can change them after creating them.
- Indexing starts at 0, so `fruits[0]` is "apple". Negative indexes count from the end: `fruits[-1]` is "cherry".
- `fruits.append("mango")` adds an item to the end. `len(fruits)` gives the number of items.

## Dictionaries
A dictionary stores **key-value pairs** inside curly braces: `student = {"name": "Riya", "age": 16}`.
You read a value with its key: `student["name"]` gives "Riya".

## Tuples
A tuple is like a list but **immutable** (cannot be changed): `point = (3, 4)`.

## Conditions
`if`, `elif` and `else` choose which code runs:
```python
if marks >= 90:
    print("A grade")
elif marks >= 75:
    print("B grade")
else:
    print("Keep practising")
```
Indentation (4 spaces) shows which lines belong inside the `if` block.

## Loops
A **for loop** repeats code for each item in a sequence:
```python
for fruit in fruits:
    print(fruit)
```
`range(5)` produces the numbers 0, 1, 2, 3, 4, so `for i in range(5)` runs 5 times.

A **while loop** repeats code as long as a condition is True:
```python
count = 0
while count < 3:
    count = count + 1
```
`break` stops a loop early; `continue` skips to the next round. A common mistake is a while loop
whose condition never becomes False - this is called an infinite loop.

## Functions
A function is a reusable block of code defined with `def`:
```python
def greet(name):
    return "Hello " + name
```
`name` is a **parameter**. `return` sends a value back to whoever called the function.
Functions help avoid repeating code (the DRY principle: Don't Repeat Yourself).
