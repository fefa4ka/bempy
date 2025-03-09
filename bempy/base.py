from inspect import getfullargspec
from typing import List, Dict, Any, Optional, Tuple


class Block:
    """
    The base Block class that all BEM blocks inherit from.
    
    This class provides the foundation for creating BEM blocks with modifiers.
    It handles initialization, inheritance, and string representation.
    
    Attributes:
        scope (list): Global BEM scope that tracks all block instances.
        owner (list): Tracks the current active block.
        files (List[str]): List of source files used in building the block.
        inherited (list): List of block classes that this block inherits from.
    """
    # Global BEM scope
    scope = []

    # Active block
    owner = [None]

    # List of source files used in block building
    files: List[str] = ['base.py']

    # List of inherited block classes
    # Another block could be inherited in different maniere:
    # * Inherit certain modification `class SomeBlock(InheritedBlock(mod='certain'))`
    # * inherited prop add ability to use any iherited modification
    inherited = []

    def __init__(self, *args, **kwargs):
        """
        Initialize Block instance and perform required setup.
        
        This method sets up the block in the global scope, initializes all models,
        and passes the appropriate arguments to each model's init method.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments that will be passed to the init method
                     of each model in the block.
        """
        # Update the global scope with the current block instance
        if not len(self.scope):
            self.root = True

        # Previous block, if they didn't release, owner of current instance
        self.scope.append((self.owner[-1], self))
        self.owner.append(self)

        for cls in self.models:
            mount_args_keys = getfullargspec(cls.init).args
            if len(mount_args_keys) == 1:
                args = []

            mount_args = {key: value for key, value in kwargs.items()
                          if key in mount_args_keys}
            cls.init(self, *args, **mount_args)

        self.owner.pop()

    def __str__(self) -> str:
        """
        Returns a string representation of the block.
        
        The string includes the block name, modifiers, and a unique identifier.
        
        Returns:
            str: A formatted string representing the block.
        """
        if hasattr(self, '__pretty_name'):
            return self.__pretty_name

        name: List[str] = []
        for word in getattr(self, 'name', '').split('.'):
            name.append(word.capitalize())

        for key, value in getattr(self, 'mods', {}).items():
            name.append(' '.join([key.capitalize()] + [str(el).capitalize()
                                                       for el in value]))

        block_name: str = str(id(self)) # codenamize(id(self), 0)
        name.append('#' + block_name)

        self.__pretty_name = ' '.join(name)

        return self.__pretty_name

    def __repr__(self) -> str:
        """
        Returns a string representation of the block (same as __str__).
        
        Returns:
            str: A formatted string representing the block.
        """
        return str(self)
