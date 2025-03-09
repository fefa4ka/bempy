# BEMPy Documentation

Welcome to the BEMPy documentation! This documentation provides comprehensive information about the BEMPy library, including API reference, usage examples, and best practices.

## Contents

- [API Documentation](api/index.md) - Comprehensive reference for all public classes and functions
- [Implementation Guide](../IMPLEMENTATION_PLAIN.md) - Detailed explanation of the BEMPy implementation

## Quick Start

To get started with BEMPy, install the library using pip:

```bash
pip install bempy
```

Then, import the necessary components:

```python
from bempy import Block, bem_scope
from bempy.builder import Build
```

Define your block scope:

```python
bem_scope('./blocks')
```

Create a block instance:

```python
my_block = Build('example/MyBlock', modifier='value')(arg1='value1')
```

## Examples

Check out the [examples directory](../tests/blocks) for complete examples of BEM blocks.

## Contributing

Contributions to the documentation are welcome! Please submit a pull request with your changes.
