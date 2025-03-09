# Scope Functions

BEMPy provides functions for defining and managing the scope of BEM blocks.

## Functions

### `bem_scope(root='./blocks')`

Scans a directory structure to find available blocks and their modifiers.

**Parameters:**
- `root (str, optional)`: The root directory to scan for blocks. Defaults to './blocks'.

**Returns:**
- `dict`: A dictionary containing the available blocks and their modifiers

**Example:**
```python
from bempy import bem_scope

# Get all blocks in the default directory
blocks = bem_scope()

# Get blocks from a specific directory
blocks = bem_scope('./my_blocks')
```

### `bem_scope_module(scopes, root='')`

Creates module-level imports for blocks.

**Parameters:**
- `scopes (dict)`: A dictionary of scopes
- `root (str, optional)`: The root module name. Defaults to ''.

**Example:**
```python
from bempy import bem_scope, bem_scope_module

# Get all blocks
blocks = bem_scope()

# Create module-level imports
bem_scope_module(blocks)

# Now you can import blocks directly
from bempy.game import Character
```

### `get_created_blocks(block_type: Optional[str])`

Returns a dictionary of created block instances of the specified type.

**Parameters:**
- `block_type (Optional[str])`: The type of blocks to return. If None, returns all blocks.

**Returns:**
- `dict`: A dictionary of block instances

**Example:**
```python
from bempy import get_created_blocks, Block

# Get all created blocks
all_blocks = get_created_blocks(None)

# Get blocks of a specific type
my_blocks = get_created_blocks(Block)
```
