# liteexpr

A light, expression language.


## Language Overview

For the language overview, see the [main page](..).
The rest of the document describes using liteexpr with Python.


## Installation

```sh
pip3 install liteexpr
```


## Example

```python
import liteexpr

symbols = liteexpr.LE_SymbolTable({
    "grades" : {
        "alice" : "A",
        "bob"   : "B",
    }
})

liteexpr.eval("""
    PRINT("I have " + LEN(grades) + " students");
    PRINT("Alice's grade is " + grades.alice);
""", symbols)
```

Output:

```
I have 2 students
Alice's grade is A
```


## License

[Apache 2.0](../LICENSE)

