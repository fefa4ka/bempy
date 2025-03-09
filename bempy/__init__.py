import builtins
import glob
import importlib
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional, Dict, Any, Type

from .base import Block
from .builder import Build
from .utils import merge


def get_created_blocks(block_type: Optional[Type] = None) -> Dict[str, Any]:
    """
    Returns a dictionary of created block instances of the specified type.
    
    Args:
        block_type (Optional[Type]): The type of blocks to return. If None, returns all blocks.
        
    Returns:
        Dict[str, Any]: A dictionary of block instances with their references as keys.
    """
    blocks = {}

    for pair in Block.scope:
        if issubclass(pair[1].__class__, block_type or Block):
            block = pair[1]
            blocks[block.ref] = block

    return blocks


def bem_scope(root: str = './blocks') -> Dict[str, Dict[str, Any]]:
    """
    Scans a directory structure to find available blocks and their modifiers.
    
    Args:
        root (str, optional): The root directory to scan for blocks. Defaults to './blocks'.
        
    Returns:
        Dict[str, Dict[str, Any]]: A dictionary containing the available blocks and their modifiers.
        
    Example:
        >>> blocks = bem_scope('./my_blocks')
        >>> print(blocks['game']['Character']['gender'])
        ['male', 'female', 'non-binary']
    """
    blocks = defaultdict(dict)

    # Get Blocks from current root scopes
    if os.path.isdir(root):
        scopes = [ name for name in os.listdir(root) if os.path.isdir(os.path.join(root, name)) ]
        scopes = [ name for name in scopes if name[0].islower() ]
    else:
        return {}

    for scope in scopes:
        # Get Blocks from current root
        scope_root = root + '/' + scope
        for file in glob.glob(scope_root + '/*/__init__.py'):
            tail = file.split('/')
            element = tail[-2]
            if not element[0].isupper():
                continue

            blocks[scope][element] = defaultdict(list)

            for mod_type, mod_value in [(mod.split('/')[-2], mod.split('/')[-1]) for mod in glob.glob(scope_root + '/%s/_*/*.py' % element)]:
                if mod_value.find('_test.py') != -1:
                    continue

                mod_type = mod_type[1:]
                mod_value = mod_value.replace('.py', '')

                blocks[scope][element][mod_type].append(mod_value)

            blocks[scope][element] = dict(blocks[scope][element])

        inner_blocks = bem_scope(scope_root)
        blocks[scope] = {
            **blocks[scope],
            **inner_blocks
        }

    return dict(blocks)


def bem_scope_module(scopes: Dict[str, Any], root: str = '') -> None:
    """
    Creates module-level imports for blocks.
    
    This function makes blocks available for import directly from the bempy namespace.
    
    Args:
        scopes (Dict[str, Any]): A dictionary of scopes, typically from bem_scope().
        root (str, optional): The root module name. Defaults to ''.
        
    Example:
        >>> bem_scope_module(bem_scope())
        >>> from bempy.game import Character
    """
    blocks = defaultdict(dict)

    # Get Blocks from current root scopes
    scopes_keys = [ name for name in scopes.keys() if name[0].islower() ]
    blocks_keys = [ name for name in scopes.keys() if name[0].isupper() ]

    for scope in scopes_keys:
        bem_scope_module(scopes[scope], '.'.join([root, scope]))

    for block in blocks_keys:
        def build(name=root[1:] + '.' + block, *arg, **kwarg):
            return Build(name, *arg, **kwarg).block

        blocks[block] = build

    if root:
        sys.modules[__name__ + root] = type(root, (object,), blocks)

# Path to the built-in blocks
module_blocks = os.path.dirname(__file__) + '/blocks/'

# Merge built-in blocks with user blocks
bem_scope_dict = merge(
    bem_scope(module_blocks),
    bem_scope()
)

# Make blocks available for import
bem_scope_module(bem_scope_dict)

