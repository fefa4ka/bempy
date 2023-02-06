from inspect import getfullargspec
from typing import List


class Block:
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

    def __str__(self):
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

    def __repr__(self):
        return str(self)
