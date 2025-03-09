from inspect import getmro
from os import path
from typing import List, Dict, Any, Tuple, Type, Optional

from .base import Block as BaseBlock
from .utils import uniq_f7, safe_serialize
from .utils.structer import (get_block_class, get_mod_classes, mods_from_dict,
                             mods_predefined)

ModsType = Dict[str, List[str]]

class Build:
    """
    The Build class is responsible for constructing BEM components with their modifiers.
    
    This class handles block initialization, inheritance, and file tracking.
    It provides methods for creating block instances with specific modifiers.
    
    Attributes:
        name (str): The name of the block.
        mods (ModsType): A dictionary of modifiers applied to the block.
        props (ModsType): A dictionary of properties passed to the block.
        models (list): A list of model classes that make up the block.
        inherited (list): A list of inherited block classes.
        files (List[str]): A list of source files used in building the block.
    """
    
    def __init__(self, name: str, *args, **kwargs: ModsType):
        """
        Initializes a Build object with the given name and modifiers.

        Args:
            name (str): The name of the block to build.
            *args: Variable length argument list.
            **kwargs (ModsType): Keyword arguments that represent the modifiers to apply to the block.
        """
        self.name: str = name
        self.mods: ModsType = {}
        self.props: ModsType = {}
        self.models = []
        self.inherited = []
        self.files: List[str] = []

        # Retrieve the base block class and file path
        base_file:str
        base_file, self.base = get_block_class(self.name)

        # If the base block does not exist, set properties directly and return
        if not self.base:
            self.props = kwargs
            return

        # Base Class that called

        # Class could maked from prebuilded Block
        # Class could inherit some class

        # Base Composed
        # InheritedBase + InheritedBase Modificator
        # BlockBase + BlockBase Modificator

        # Initialize the list of base classes
        bases = [self.base]

        # Combine predefined and provided modifiers
        request_mods = {
            **mods_predefined(self.base),
            **mods_from_dict(kwargs)
        }
        request_mods_json = safe_serialize(request_mods)
        self.mods = {}

        # Check for inherited blocks
        if hasattr(self.base, 'inherited'):
            mod_files, mod_classes, mods_loaded = get_mod_classes(self.name, request_mods_json)
            for cls in mod_classes:
                request_mods = {
                    **request_mods,
                    **mods_predefined(cls)
                }

            # Ensure inherited is a list
            self.inherited = self.base.inherited
            if not isinstance(self.base.inherited, list):
                self.inherited = [self.base.inherited]

            # Add inherited blocks to bases
            for model in self.inherited:
                block_base = model(**request_mods)
                bases.append(block_base)

        # Set the name of the base block
        self.base.name = self.name
        base_compound = []

        # Process each base class
        for index, base in enumerate(bases):
            base_file, base_cls = get_block_class(base.name)

            # Skip if the base class is already included in models
            if hasattr(self.base, 'models') and base_cls in self.base.models:
                # FIX: How recompoud if mods changed?
                # Maybe add only mod_class that not available
                # Is it possible remove old Modificators
                # Get position of original, detect available Modificators
                continue

            files = [str(base_file)]

            request_mods = {
                **mods_predefined(base_cls),
                **request_mods,
            }
            request_mods_json = safe_serialize(request_mods)
            mod_files, mod_classes, mods_loaded = get_mod_classes(base.name, request_mods_json)
            for cls in mod_classes:
                request_mods = {
                    **mods_predefined(cls),
                    **request_mods,
                }

            for file in mod_files:
                if file not in files:
                    files.append(file)

            base_models = []
            if hasattr(base, 'models'):
                base_models = list(base.models)
                if index == 0:
                    base_compound = mod_classes
            else:
                base_models = [base]
                base_models += mod_classes

            base_models.reverse()
            for model in base_models:
                if model not in self.models:
                    self.models.append(model)

            self.mods = { **self.mods,
                         **mods_loaded }

            if hasattr(base, 'files') and isinstance(base.files, list):
                for file in base.files:
                    if file not in files:
                        files.append(file)

            self.files += files

        if self.base not in self.models:
            is_modified = False
            base_compound_models = []
            for model in base_compound:
                if model not in self.models:
                    is_modified = True
                    base_compound_models.append(model)

            if is_modified:
                self.models.reverse()
                self.models.append(self.base)
                self.models += base_compound_models
                self.models.reverse()
            else:
                self.models.insert(0, self.base)

        for mod in request_mods:
            if mod not in self.mods:
                prop = request_mods[mod]
                if not isinstance(prop, list):
                    prop = [prop]

                self.props[mod] = prop

    def blocks(self) -> Tuple:
        """
        Returns a tuple of model classes that make up the block.
        
        Returns:
            tuple: A tuple of model classes.
        """
        if self.base:
            Models = self.models.copy()

            Models.reverse()
        else:
            Models = [BaseBlock]

        return tuple(Models)

    @property
    def block(self) -> Type:
        """
        Returns a new block type with the specified name, modifiers, and properties.
        
        This property creates a new class dynamically with the appropriate inheritance
        and attributes.
        
        Returns:
            Type: A dynamically created block class.
        """
        self.inherited = []

        self.files.reverse()
        self.files = uniq_f7(self.files)
        self.files.reverse()

        Block = type(self.name,
                     tuple(self.models),
                     {
                         'name': self.name,
                         'mods': self.mods,
                         'props': self.props,
                         'files': self.files,
                     })

        Block.classes = list(getmro(Block))
        Block.models = self.blocks()

        return Block


