# file structure
file extension .sigma or file has `!>sigma` as the first line

# conditionals

```bash
if (<statement>) then do
    expression
    expression
elif (<statement>) then do
    expression
else do
    expression
fi
```

## example
sigmalang: 
```bash
if (x is greater than 10) then do
    print "x is large"
elif (x is equal to 10) then do
    print "x is 10"
else do
    print "x is small"
fi
```
python equivalent:
```python
if x > 10:
    print("x is large")
elif x == 10:
    print("x is equal to 10")
else:
    print("x is small")
```

# variable assignment
variables are stored as a dictionary (globals.py > variables)

## assigning
```bash
let <type> var <name> be <expression>
let <type> const <name> be <expression> 
```

## reassigning 
```bash
change <name> to <value>
```

## examples
sigmalang:
```bash
let variable int count be 5
let constant string message be "hello, world!"
change count to 10
```
python equivalent:
```python
count: int = 5
message: str = "hello, world!"
count = 10
```

# data types
integer: whole numbers (`1`, `42`)  
float: decimals (`3.14`, `2.71`)  
boolean: `true` or `false`  
nonetype: `none` or `nothing`  
string: any text enclosed in double quotes (`"hello, world!"`)  

note: strings can include variables by using ${variablename}  
eg:  
`print "the count is ${count}"`

# comment
comments are surrounded by `<--` and `-->`
```bash
<-- comments -->
```

# loop
## while

```bash
while (<condition>) do
    expression
elihw
```

## examples
sigmalang:
```bash
while (count is greater than 0) do
    print "count: ${count}"
    change count to (count minus 1)
elihw
```
python equivalent:
```python
while count > 0:
    print(f"count {count}")
    count -= 1
```

# logic
all logic should be between brackets

greater than or equal to (>=)
```bash
<statement> is greater than or equal to <statement>
```

less than or equal to (<=)
```bash
<statemnet> is less than or equal to <statement>
```

equals to (==)

```bash
<statement> equals <statement>
```

greater than (>)
```bash
<statement> is greater than <statement>
```

less than (<)
```bash
<statement> is less than <statement>
```

not equals to (!=)
```bash
<statement> is not <statement>
```

## logical operators
and: `and`  
or: `or`  
not: `not`  

## example
sigmalang:
```bash
if ((x is greater than 5) and (y is less than 10)) then do
    print "x and y are in range"
```
python equivalent:
```python
if x > 5 and y < 10:
    print("x and y are in range")
```

# printing
sigmalang:
```bash
print "print without newline"
print line "print with newline"
```
python equivalent
```python
print("print without newline", end="")
print("print with newline")
```

# receiving input
input
```bash
receive to variable
```
## example
```bash
print "input username: "
receive to username
print "welcome, ${username}"
```

# try except
```bash
try do
    expression
except do
    expression
yrt
```

# TO BE ADDED
# functions
```bash
function foo (<param> as <type>) as
    expression
end function
```
