# bempy - Python Block-Element-Modifier Library
`bempy` is a library for building complex classes using BEM (Block-Element-Modifier) methodology. BEM is a widely used methodology in web development to achieve modular and scalable front-end code. `pybem` **extends this methodology to other areas** of software development, making it a versatile and powerful tool *for organizing and structuring complex projects*.

With `bempy`, you can build reusable blocks of code that can be easily inherited, modified, and extended to create new and complex classes. The library uses a hierarchical structure to define blocks, elements, and modifiers, making it simple to understand and maintain large projects.

## Features
* Simple and easy-to-use syntax for defining blocks, elements, and modifiers
* Support for inheritance, allowing blocks to inherit and extend the properties of other blocks
* Ability to define default arguments and properties for blocks, making it easier to create instances of blocks
* Support for automatic documentation extraction, allowing you to easily keep track of the purpose and usage of blocks and their components
* A flexible structure

## Concept
`bempy` is a library for building complex classes based on the BEM methodology. The BEM methodology is a way to structure the code for complex projects that require scalable and maintainable architecture.

The blocks are stored in a specific directory structure:
```
blocks/
    category/
        SimpleBlock/
            __init__.py
        ComplexBlock/
            _mod/
                minimal.py
                cheap.py
                extended.py
```

Each block has its own directory and `__init__.py` file. In the example, there is a `SimpleBlock` and a `ComplexBlock`.

The `SimpleBlock` class is defined in `SimpleBlock/__init__.py`:
```python
from bempy import Block

class Base(Block):
    """
        Basic block. It accept argument 'some_arg' and have parameter 'some_param'.
    """
    some_param = 31337

    def prepare(self, some_arg="str"):
        """
            some_param -- param description parsed by BEM Block
        """

        print(self.name + ': Base prepare with param =', some_arg)
```


The `ComplexBlock` class is defined in `ComplexBlock/__init__.py`:
```python
from bempy.example import Child

class Base(Child()):
    complex_param = 'lala'

    def prepare(self):
        print(self.name + ':', 'Complex prepare')
```

The `ComplexBlock` can have modificators which are stored in the `_mod` directory. In the example, there is a `minimal` modificator defined in `ComplexBlock/_mod/minimal.py`:
```python
class Modificator:
    def prepare(self, small_mod_arg=0):
        print(self.name + ':', 'Small modificator preapre with small_mod_arg =', small_mod_arg)
```

Now, you can export and build the block. To build a ComplexBlock with the minimal modificator, you can do:
```python
from bem.category import SimpleBlock, ComplexBlock

MinimalComplexBlock = ComplexBlock(mod='minimal')
complex_instance = MinimalComplexBlock(
    someArg='hello',
    extendedArg='world'
)
simple_instance = SimpleBlock()(simpleArg='first')
```
In this example, `MinimalComplexBlock = ComplexBlock(mod='minimal')` is the construction of a complex class with the specified modificator. And `MinimalComplexBlock(...)` is creating an instance of the defined block.

