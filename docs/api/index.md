# BEMPy API Documentation

This documentation provides a comprehensive reference for all public classes and functions in the BEMPy library.

## Core Modules

- [Block](block.md) - The base Block class that all BEM blocks inherit from
- [Builder](builder.md) - The Build class for constructing BEM components
- [Utilities](utils.md) - Utility functions for working with BEM components

## Getting Started

To use BEMPy, you typically start by importing the necessary components:

```python
from bempy import Block, bem_scope
from bempy.builder import Build
```

Then you can define your block scope and create block instances:

```python
# Set the scope to look for blocks
bem_scope('./blocks')

# Create a block instance
my_block = Build('example/MyBlock', modifier='value')(arg1='value1')
```

## Module Structure

BEMPy is organized into several modules:

- `bempy` - The main package containing core functionality
- `bempy.base` - Contains the Block base class
- `bempy.builder` - Contains the Build class for constructing blocks
- `bempy.utils` - Contains utility functions
- `bempy.utils.structer` - Contains block and modifier lookup functions
