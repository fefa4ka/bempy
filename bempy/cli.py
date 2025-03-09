#!/usr/bin/env python3
"""
BEMPy Command Line Interface

This module provides a command-line interface for working with BEMPy projects.
It allows users to create, list, and manage BEM blocks and modifiers.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

from bempy import bem_scope


def create_block(name: str, path: str = './blocks') -> None:
    """
    Creates a new BEM block with the specified name.
    
    Args:
        name (str): The name of the block (e.g., 'game/Character').
        path (str, optional): The path to the blocks directory. Defaults to './blocks'.
    """
    parts = name.split('/')
    if len(parts) < 2:
        print(f"Error: Block name must be in the format 'scope/BlockName'")
        return
    
    scope = parts[0]
    block_name = parts[1]
    
    if not block_name[0].isupper():
        print(f"Error: Block name '{block_name}' must start with an uppercase letter")
        return
    
    block_dir = os.path.join(path, scope, block_name)
    os.makedirs(block_dir, exist_ok=True)
    
    init_file = os.path.join(block_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write(f"""from bempy import Block

class Base(Block):
    \"\"\"
    A basic {block_name} implementation
    \"\"\"

    def init(self, param1=None):
        \"\"\"
        param1 -- Description of param1
        \"\"\"
        
        print(self.name + ': {block_name} created with param1 =', param1)
""")
        print(f"Created block '{name}' at {block_dir}")
    else:
        print(f"Block '{name}' already exists at {block_dir}")


def create_modifier(block_name: str, mod_type: str, mod_value: str, path: str = './blocks') -> None:
    """
    Creates a new modifier for a BEM block.
    
    Args:
        block_name (str): The name of the block (e.g., 'game/Character').
        mod_type (str): The type of the modifier (e.g., 'gender').
        mod_value (str): The value of the modifier (e.g., 'female').
        path (str, optional): The path to the blocks directory. Defaults to './blocks'.
    """
    parts = block_name.split('/')
    if len(parts) < 2:
        print(f"Error: Block name must be in the format 'scope/BlockName'")
        return
    
    scope = parts[0]
    block = parts[1]
    
    block_dir = os.path.join(path, scope, block)
    if not os.path.exists(os.path.join(block_dir, '__init__.py')):
        print(f"Error: Block '{block_name}' does not exist")
        return
    
    mod_dir = os.path.join(block_dir, f'_{mod_type}')
    os.makedirs(mod_dir, exist_ok=True)
    
    mod_file = os.path.join(mod_dir, f'{mod_value}.py')
    if not os.path.exists(mod_file):
        with open(mod_file, 'w') as f:
            f.write(f"""class Modificator:
    \"\"\"
    A {mod_value} {mod_type} implementation
    \"\"\"

    def init(self, param1=None):
        \"\"\"
        param1 -- Description of param1
        \"\"\"
        
        print(self.name + ': {mod_value.capitalize()} {mod_type} created with param1 =', param1)
""")
        print(f"Created modifier '{mod_type}={mod_value}' for block '{block_name}'")
    else:
        print(f"Modifier '{mod_type}={mod_value}' for block '{block_name}' already exists")


def list_blocks(path: str = './blocks') -> None:
    """
    Lists all available BEM blocks and their modifiers.
    
    Args:
        path (str, optional): The path to the blocks directory. Defaults to './blocks'.
    """
    blocks = bem_scope(path)
    if not blocks:
        print(f"No blocks found in {path}")
        return
    
    for scope, scope_blocks in blocks.items():
        print(f"{scope}:")
        for block, mods in scope_blocks.items():
            print(f"  {block}:")
            for mod_type, mod_values in mods.items():
                print(f"    {mod_type}: {', '.join(mod_values)}")


def main() -> None:
    """
    Main entry point for the BEMPy CLI.
    """
    parser = argparse.ArgumentParser(description='BEMPy Command Line Interface')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Create block command
    create_block_parser = subparsers.add_parser('create-block', help='Create a new BEM block')
    create_block_parser.add_argument('name', help='Name of the block (e.g., game/Character)')
    create_block_parser.add_argument('--path', default='./blocks', help='Path to the blocks directory')
    
    # Create modifier command
    create_mod_parser = subparsers.add_parser('create-modifier', help='Create a new modifier for a BEM block')
    create_mod_parser.add_argument('block', help='Name of the block (e.g., game/Character)')
    create_mod_parser.add_argument('type', help='Type of the modifier (e.g., gender)')
    create_mod_parser.add_argument('value', help='Value of the modifier (e.g., female)')
    create_mod_parser.add_argument('--path', default='./blocks', help='Path to the blocks directory')
    
    # List blocks command
    list_blocks_parser = subparsers.add_parser('list', help='List all available BEM blocks')
    list_blocks_parser.add_argument('--path', default='./blocks', help='Path to the blocks directory')
    
    args = parser.parse_args()
    
    if args.command == 'create-block':
        create_block(args.name, args.path)
    elif args.command == 'create-modifier':
        create_modifier(args.block, args.type, args.value, args.path)
    elif args.command == 'list':
        list_blocks(args.path)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
