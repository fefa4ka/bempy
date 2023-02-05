# bempy - Python Block-Element-Modifier Library
`bempy` is a library for building complex classes using BEM (Block-Element-Modifier) methodology.

With `bempy`, you can build reusable blocks of code that can be easily inherited, modified, and extended to create new and complex classes. The library uses a hierarchical structure to define blocks, elements, and modifiers, making it simple to understand and maintain large projects.

## Features
* Simple and easy-to-use syntax for defining blocks, elements, and modifiers
* Support for inheritance, allowing blocks to inherit and extend the properties of other blocks
* Ability to define default arguments and properties for blocks, making it easier to create instances of blocks
* Support for automatic documentation extraction, allowing you to easily keep track of the purpose and usage of blocks and their components
* A flexible structure

## Concept
`bempy` is a library for building complex classes based on the BEM methodology.

### BEM
BEM, or Block Element Modifier, is a methodology that helps developers build scalable, maintainable and reusable components for their projects.

The main idea behind BEM is to encapsulate appearance, logic and content of a component into distinct blocks that can be easily re-used and modified without affecting the rest of the application. Each block is treated as an independent entity and can be combined with other blocks to create complex structures.

In BEM, a block is the main building block of the application, and it can consist of multiple elements and modifiers. An element is a part of a block that cannot be used independently, and it provides additional functionality and styling to the block. A modifier is a variation of a block or element that changes its appearance or behavior.

Using BEM helps to create well-structured, modular and maintainable code that can be easily adapted to changing requirements. It also makes it easier for developers to collaborate on a project, as each block can be worked on independently and the resulting code is easy to understand and integrate into the rest of the application.

### BEM Python
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
    some_arg='hello',
    small_mod_arg='world'
)
simple_instance = SimpleBlock()(some_arg='first')
```
In this example, `MinimalComplexBlock = ComplexBlock(mod='minimal')` is the construction of a complex class with the specified modificator. And `MinimalComplexBlock(...)` is creating an instance of the defined block.


## Installation
You can install `bempy` library via `pip` by running the following command in your terminal:
```
pip install bempy
```

After installation, you can import the library in your Python code by using:
```
import bempy
```

You can also install the latest version of the library directly from the source code by cloning the repository and running the following command:
`python setup.py install`


## Use Cases
`bempy` has a wide range of use cases, beyond the original intended purpose of helping developers build complex UI components. Here are a few examples of how BEMPy can be applied:
* **Data Science**: To data science projects to help structure and organize code. By breaking down data processing into blocks, it becomes easier to create and maintain complex data pipelines.
* **Scientific Computing**: To structure complex mathematical models in a way that makes them more understandable, manageable and maintainable.
* **Game Development**: The BEM methodology provides a way to structure game objects in a way that makes them easier to manage and maintain.
* **API Development**: To build APIs that are easy to consume and understand. By breaking down a complex system into blocks and applying modularization techniques, it becomes easier to test, debug and maintain the API.
* **Front-end Development**: To write clean, scalable and maintainable HTML, CSS and JavaScript for web front-end development. BEM methodology helps to encapsulate styles and behavior into blocks, making it easy to build and reuse UI components.
* **Back-end Development**: By using BEM methodology to structure and organize code, it becomes easier to create and maintain complex systems.

In each of these cases, **bempy**'s structure and methodology helps developers to create complex systems that are maintainable and scalable over time. Whether you are working on a small project or a large enterprise application, `bempy` can help you write clean, modular and maintainable code.

## Contributing
I'm appreciate and welcome contributions to `bempy`. If you are interested in contributing, there are several ways to get started:
* **Report a bug**: If you find a bug or an issue in the library, please open an issue in the Github repository with a description of the problem and steps to reproduce it.
* **Fix a bug**: If you have a fix for a bug, please submit a pull request with a description of the bug and how you fixed it.
* **Implement a new feature**: If you want to add a new feature to the library, please open an issue in the Github repository to discuss your idea and the implementation details. After the discussion, you can submit a pull request with your implementation.
* **Improve documentation**: If you see an opportunity to improve the documentation, feel free to submit a pull request with changes.
* **Test the library**: If you have time, you can help us by testing the library and submitting bug reports or even fixes.

## License
The `bempy` library is licensed under the terms of the GNU General Public License v3.0 (GPL-3.0). This means that you have the freedom to use, modify, and distribute the software and its source code.

By contributing to `bempy`, you agree to license your contributions under the same terms. This allows everyone to benefit from your contributions, while also protecting the future of the project.

## References
These references provide additional information on BEM methodology and its implementation in various technologies. They can help you understand the concept and best practices of BEM and provide guidance on how to apply it in your work:
* BEM (Block Element Modifier) Methodology - https://en.bem.info/methodology/
* CSS BEM - https://css-tricks.com/bem-101/
* BEM Naming Convention - https://en.bem.info/methodology/naming-convention/
* BEM Metodology in React - https://github.com/bem/bem-react
* BEM Components Library - https://github.com/bem/bem-components
* BEM Tools - https://en.bem.info/tools/

