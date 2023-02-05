import json
from collections import OrderedDict
from functools import lru_cache
from inspect import currentframe, getmro
from os import path
from typing import Any, List, Optional, Union, cast, Dict

from .base import Block as BaseBlock
from .utils import uniq_f7
from .utils.args import default_arguments, safe_serialize
from .utils.structer import (get_block_class, get_mod_classes, mods_from_dict,
                             mods_predefined)

ModsType = Dict[str, List[str]]


class Build:
    def __init__(self, name: str, *args, **kwargs: ModsType):
        self.name: str = name
        self.mods: ModsType = {}
        self.props: ModsType = {}
        self.models = []
        self.inherited = []
        self.files: List[str] = []

        base_file:str
        base_file, self.base = get_block_class(self.name)

        if not self.base:
            self.props = kwargs
            return

        # Base Class that called

        # Class could maked from prebuilded Block
        # Class could inherit some class

        # Base Composed
        # InheritedBase + InheritedBase Modificator
        # BlockBase + BlockBase Modificator

        bases = [self.base]

        request_mods = {
            **mods_predefined(self.base),
            **mods_from_dict(kwargs)
        }
        request_mods_json = safe_serialize(request_mods)
        self.mods = {}

        #classes = list(getmro(self.base))[:-1]
        if hasattr(self.base, 'inherited'):
            mod_files, mod_classes, mods_loaded = get_mod_classes(self.name, request_mods_json)
            for cls in mod_classes:
                request_mods = {
                    **request_mods,
                    **mods_predefined(cls)
                }

            self.inherited = self.base.inherited
            if not isinstance(self.base.inherited, list):
                self.inherited = [self.base.inherited]

            for model in self.inherited:
                block_base = model(**request_mods)
                bases.append(block_base)

        self.base.name = self.name
        base_compound = []

        for index, base in enumerate(bases):
            base_file, base_cls = get_block_class(base.name)

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

    def blocks(self):
        if self.base:
            Models = self.models.copy()

            Models.reverse()
        else:
            Models = [BaseBlock]

        return tuple(Models)

    @property
    def block(self):
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
        Block.arguments, Block.defaults = default_arguments(Block)

        return Block

