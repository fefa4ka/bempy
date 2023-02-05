import builtins
import glob
import importlib
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional

from .base import Block
from .builder import Build
from .utils import merge


def get_created_blocks(block_type: Optional[str]):
    blocks = {}

    for pair in Block.scope:
        if issubclass(pair[1].__class__, block_type or Block):
            block = pair[1]
            blocks[block.ref] = block

    return blocks


def bem_scope(root='./blocks'):
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


def bem_scope_module(scopes, root=''):
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

module_blocks = os.path.dirname(__file__) + '/blocks/'

bem_scope_dict = merge(
    bem_scope(module_blocks),
    bem_scope()
)

bem_scope_module(bem_scope_dict)

