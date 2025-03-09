from importlib import import_module
from os import getenv
from os.path import dirname
from pathlib import Path
from inspect import getmro
from typing import List, Dict, Any, Tuple, Type, Optional
import json
from functools import lru_cache


def bem_blocks_path() -> str:
    """
    Returns the path to the directory containing the BEM blocks.
    
    Returns:
        str: The path to the blocks directory.
    """
    module_path = dirname(__file__)
    blocks_path = str(Path(module_path).parent / Path('blocks'))

    return blocks_path

@lru_cache
def get_block_class(name: str) -> Tuple[Optional[Path], Optional[Type]]:
    """
    Retrieves a block class by name (cached).
    
    This function is a cached wrapper around lookup_block_class.
    
    Args:
        name (str): The name of the block.
        
    Returns:
        Tuple[Optional[Path], Optional[Type]]: A tuple containing the path to the base file and the block class.
    """
    return lookup_block_class(name)

def lookup_block_class(name: str, libraries: List[str]=[]) -> Tuple[Optional[Path], Optional[Type]]:
    """
    Looks up the block class for the given block name.

    Args:
        name (str): The name of the block.
        libraries (List[str], optional): A list of library names to search for the block. Defaults to [].

    Returns:
        Tuple[Optional[Path], Optional[Type]]: A tuple containing the path to the base file and the block class.
    """
    bem_blocks = bem_blocks_path()
    libraries += getenv('BEM_LIBRARIES') or ['blocks']
    libraries.append(bem_blocks)

    # Convert slashes to dots for module import but keep original for path
    module_name = name.replace('/', '.')
    block_dir = name.replace('.', '/')
    base_file = block_class = module_path = None

    for lib in libraries:
        base_file = Path(lib) / block_dir / ('__init__.py')

        if base_file.exists():
            if lib == bem_blocks:
                module_path = 'bem.blocks'
            else:
                module_path = lib

            break

    if base_file and base_file.exists():
        block_class = import_module(module_path + '.' + module_name).Base
    else:
        return None, None

    return base_file, block_class


def mods_from_dict(kwargs: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Converts a dictionary of modifications to a dictionary of lists.

    Args:
        kwargs (Dict[str, Any]): A dictionary of modifications. The values can be either a string divided by commas or a list.

    Returns:
        Dict[str, List[str]]: A dictionary of modifications with values as lists.
    """
    mods = {}

    for mod, value in kwargs.items():
        if isinstance(value, list):
            mods[mod] = value
        else:
            if isinstance(value, str):
                value = value.split(',')
            else:
                value = [value]

            mods[mod] = value

    return mods


def mods_predefined(base: Type) -> Dict[str, List[str]]:
    """
    Returns a dictionary of predefined modifications for the given block class.

    Args:
        base (Type): The block class.

    Returns:
        Dict[str, List[str]]: A dictionary of predefined modifications.
    """
    mods = {}

    classes = list(getmro(base))[:-1]
    # Clear builder duplicates
    classes = [cls for cls in classes if 'builder' not in str(cls)]
    classes.reverse()

    for cls in classes:
        if hasattr(cls, 'mods'):
            for mod, value in cls.mods.items():
                if not mods.get(mod, None):
                    mods[mod] = value

    return mods

@lru_cache
def get_mod_classes(name: str, selected_mods: str) -> Tuple[List[str], List[Type], Dict[str, List[str]]]:
    """
    Retrieves modifier classes for a block (cached).
    
    This function is a cached wrapper around lookup_mod_classes.
    
    Args:
        name (str): The name of the block.
        selected_mods (str): A JSON string representing the selected modifiers.
        
    Returns:
        Tuple[List[str], List[Type], Dict[str, List[str]]]: A tuple containing files, classes, and modifiers.
    """
    mods = json.loads(selected_mods)
    return lookup_mod_classes(name, mods)

def lookup_mod_classes(name: str, selected_mods: Dict[str, Any], libraries: List[str]=[]) -> Tuple[List[str], List[Type], Dict[str, List[str]]]:
    """
    Looks up the classes of the selected modifications.

    Args:
        name (str): The name of the block.
        selected_mods (Dict[str, Any]): A dictionary of selected modifications.
        libraries (List[str], optional): A list of libraries to search for the block. Defaults to [].

    Returns:
        Tuple[List[str], List[Type], Dict[str, List[str]]]: A tuple containing a list of files, a list of classes, and a dictionary of modifications.
    """
    bem_blocks = bem_blocks_path()
    libraries += getenv('BEM_LIBRARIES') or ['blocks']
    libraries.append(bem_blocks)

    block_dir = name.replace('.', '/')
    mod_file = module_path = None
    classes = []
    files = []
    mods = {}

    for mod, values in selected_mods.items():
        if not isinstance(values, list):
            values = [str(values)]

        for value in values:
            for lib in libraries:
                mod_file = Path(lib) / block_dir / ('_' + mod) / (str(value) + '.py')
                if mod_file.exists():
                    if lib == bem_blocks:
                        module_path = 'bem.blocks'
                    else:
                        module_path = lib

                    break

            if mod_file and mod_file.exists():
                mod_file = Path(lib) / block_dir / ('_' + mod) / (str(value) + '.py')
                Module = import_module(module_path + '.' + block_dir.replace('/', '.') + '._' + mod + '.' + value)
                classes.append(Module.Modificator)
                files.append(str(mod_file))

                if hasattr(Module.Modificator, 'files'):
                    files += Module.Modificator.files

                instance_mods = Module.Modificator.mods if hasattr(Module.Modificator, 'mods') else {}
                mods = {
                    **mods,
                    **instance_mods,
                    mod: values
                }


    return files, classes, mods

