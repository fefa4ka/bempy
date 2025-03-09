# BEMPy - Python Block-Element-Modifier Library

BEMPy is a library for building complex classes using the Block-Element-Modifier methodology. It provides a structured approach to class composition through reusable, modifiable components.

## Core Concepts

- **Blocks**: Independent entities that form the foundation of your components
- **Modifiers**: Variations that alter a block's appearance or behavior
- **Inheritance**: Blocks can inherit and extend properties from other blocks

## Installation

```bash
pip install bempy
```

## Basic Usage

```python
from bempy import bem_scope
from bempy.builder import Build

# Set the scope to look for blocks
bem_scope('./blocks')

# Create a character with modifiers
character = Build('game/Character', 
                  race='elf', 
                  gender='female', 
                  abilities=['agility'])

# Initialize the character with specific parameters
player = character(level=10, fertility=80, mana=100)
```

## Directory Structure

Blocks are organized in a specific directory structure:

```
blocks/
    game/
        Character/
            __init__.py          # Base implementation
            _gender/             # Gender modifiers
                female.py
                male.py
            _race/               # Race modifiers
                elf.py
                human.py
```

## CLI Tool

BEMPy includes a command-line tool for creating and managing blocks:

```bash
# Create a new block
bempy create-block game/Character

# Add a modifier
bempy create-modifier game/Character race elf

# List available blocks
bempy list
```

## Documentation

For detailed documentation, see:
- [API Reference](docs/api/index.md)
- [Implementation Guide](IMPLEMENTATION_PLAIN.md)

## License

GNU General Public License v3.0 (GPL-3.0)

## Author

Alexander Kondratev (alex@nder.work)
