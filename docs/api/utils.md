# Utility Functions

BEMPy provides several utility functions to help with common tasks when working with BEM components.

## General Utilities

### `merge(source, destination)`

Merges two dictionaries recursively.

**Parameters:**
- `source (dict)`: The source dictionary
- `destination (dict)`: The destination dictionary

**Returns:**
- `dict`: The merged dictionary

**Example:**
```python
from bempy.utils import merge

a = {'first': {'all_rows': {'pass': 'dog', 'number': '1'}}}
b = {'first': {'all_rows': {'fail': 'cat', 'number': '5'}}}
result = merge(b, a)
# result = {'first': {'all_rows': {'pass': 'dog', 'fail': 'cat', 'number': '5'}}}
```

### `uniq_f7(seq)`

Returns a list with duplicate elements removed while preserving order.

**Parameters:**
- `seq (list)`: The input sequence

**Returns:**
- `list`: A list with duplicate elements removed

**Example:**
```python
from bempy.utils import uniq_f7

result = uniq_f7([1, 2, 3, 2, 1, 4])
# result = [1, 2, 3, 4]
```

### `safe_serialize(obj)`

Safely serializes an object to JSON, converting non-serializable objects to strings.

**Parameters:**
- `obj`: The object to serialize

**Returns:**
- `str`: A JSON string representation of the object

**Example:**
```python
from bempy.utils import safe_serialize

class MyClass:
    pass

obj = {'name': 'test', 'instance': MyClass()}
json_str = safe_serialize(obj)
# json_str = '{"name": "test", "instance": "<__main__.MyClass object at 0x...>"}'
```

## Structure Utilities

### `bem_blocks_path()`

Returns the path to the directory containing the BEM blocks.

**Returns:**
- `str`: The path to the blocks directory

### `get_block_class(name: str)`

Retrieves a block class by name (cached).

**Parameters:**
- `name (str)`: The name of the block

**Returns:**
- `tuple`: A tuple containing the path to the base file and the block class

### `lookup_block_class(name: str, libraries: List[str]=[])`

Looks up a block class across libraries.

**Parameters:**
- `name (str)`: The name of the block
- `libraries (List[str], optional)`: A list of library names to search for the block

**Returns:**
- `tuple`: A tuple containing the path to the base file and the block class

### `mods_from_dict(kwargs)`

Converts a dictionary of modifications to a standardized format.

**Parameters:**
- `kwargs (dict)`: A dictionary of modifications

**Returns:**
- `dict`: A dictionary of modifications with values as lists

### `mods_predefined(base)`

Returns predefined modifications for a block class.

**Parameters:**
- `base`: The block class

**Returns:**
- `dict`: A dictionary of predefined modifications

### `get_mod_classes(name: str, selected_mods: str)`

Retrieves modifier classes for a block (cached).

**Parameters:**
- `name (str)`: The name of the block
- `selected_mods (str)`: A JSON string representing the selected modifiers

**Returns:**
- `tuple`: A tuple containing files, classes, and modifiers

### `lookup_mod_classes(name: str, selected_mods, libraries=[])`

Looks up modifier classes across libraries.

**Parameters:**
- `name (str)`: The name of the block
- `selected_mods (dict)`: A dictionary of selected modifiers
- `libraries (list, optional)`: A list of libraries to search for the block

**Returns:**
- `tuple`: A tuple containing a list of files, a list of classes, and a dictionary of modifications
