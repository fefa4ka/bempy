# Block Class

The `Block` class is the foundation of the BEMPy library. It serves as the base class for all BEM blocks and provides core functionality for block initialization, inheritance, and representation.

## Class Definition

```python
class Block:
    # Global BEM scope
    scope = []

    # Active block
    owner = [None]

    # List of source files used in block building
    files: List[str] = ['base.py']

    # List of inherited block classes
    inherited = []
```

## Constructor

```python
def __init__(self, *args, **kwargs)
```

Initializes a Block instance and performs required setup.

**Parameters:**
- `*args`: Variable length argument list
- `**kwargs`: Arbitrary keyword arguments that will be passed to the `init` method of each model in the block

## Methods

### `__str__(self)`

Returns a string representation of the block.

**Returns:**
- `str`: A formatted string representing the block, including its name, modifiers, and a unique identifier

### `__repr__(self)`

Returns a string representation of the block (same as `__str__`).

**Returns:**
- `str`: A formatted string representing the block

## Class Variables

### `scope`

A list that tracks all block instances in the global scope.

### `owner`

A list that tracks the current active block.

### `files`

A list of source files used in building the block.

### `inherited`

A list of block classes that this block inherits from.

## Usage Example

```python
from bempy import Block

class MyBlock(Block):
    """
    A custom block implementation
    """
    
    def init(self, param1=None):
        """
        Initialize the block with custom parameters
        
        param1 -- Description of param1
        """
        self.param1 = param1
        print(f"{self.name}: Initialized with param1={param1}")
```

## Notes

- The `init` method should be implemented by subclasses to define custom initialization behavior
- Block instances are automatically added to the global scope when created
- The `inherited` list can be used to define block inheritance relationships
