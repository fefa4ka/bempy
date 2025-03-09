# Build Class

The `Build` class is responsible for constructing BEM components with their modifiers. It handles block initialization, inheritance, and file tracking.

## Class Definition

```python
class Build:
    def __init__(self, name: str, *args, **kwargs: ModsType)
```

## Constructor

**Parameters:**
- `name (str)`: The name of the block to build
- `*args`: Variable length argument list
- `**kwargs (ModsType)`: Keyword arguments that represent the modifiers to apply to the block

## Properties

### `block`

Returns a new block type with the specified name, modifiers, and properties.

**Returns:**
- A dynamically created block class with the specified configuration

## Methods

### `blocks(self)`

Returns a tuple of model classes that make up the block.

**Returns:**
- `tuple`: A tuple of model classes

## Attributes

### `name`

The name of the block.

### `mods`

A dictionary of modifiers applied to the block.

### `props`

A dictionary of properties passed to the block.

### `models`

A list of model classes that make up the block.

### `inherited`

A list of inherited block classes.

### `files`

A list of source files used in building the block.

## Usage Example

```python
from bempy.builder import Build

# Create a server block with flask backend and debug configuration
server = Build('backend/Server', 
               backend='flask', 
               config='debug', 
               extensions=['cors', 'db'])

# Instantiate the server with specific parameters
server_instance = server(host='localhost', port=8080)
```

## Notes

- The `Build` class is responsible for looking up block classes and their modifiers
- It handles inheritance between blocks
- It tracks the files used to build the block for debugging purposes
- It manages the composition of multiple modifier classes
