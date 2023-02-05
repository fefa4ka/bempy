import sys
from inspect import currentframe, getfullargspec, getmembers, isroutine
from os import path
from sys import _getframe, setprofile
from types import FunctionType
from typing import Dict, List, Optional, Set, Tuple

from .utils.args import parse_arguments
from .utils.logger import block_params, logger_init
from .utils.parser import (block_params_description, inspect_code,
                           inspect_comments, inspect_ref)

# from codenamize import codenamize


log = logger_init(__name__)
tracer_instances = [None]

class Block:
    # Global BEM scope
    scope = []

    # Active block
    owner = [None]
    # List of block references
    refs: List[str] = []

    # List of source files used in block building
    files: List[str] = ['bem/base.py']

    # List of inherited block classes
    # Another block could be inherited in different maniere:
    # * Inherit certain modification `class SomeBlock(InheritedBlock(mod='certain'))`
    # * inherited prop add ability to use any iherited modification
    inherited = []

    # List of methods used to extract parameters descriptions
    doc_methods: List[str] = ['prepare', 'body']

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

        # Store comments about block usage
        self.notes: List[str] = []
        self.__pretty_name = None

        # Disable tracing
        setprofile(None)

        # Extract the caller context and store it
        deph = 0
        ref: str = None
        while ref is None:
            # Traversal through call stack frames for search the same instance
            frame = _getframe(deph)
            # Grab name of variable used for instance of this Block
            context = inspect_code(self, frame)
            ref = context['ref']

            # Store any comments associated with the caller
            if context.get('comment_line_start', None) is not None:
                self.notes = inspect_comments(
                    context['source'],
                    context['comment_line_start'],
                    context['comment_line_end'])

            self.context = {
                'caller': context['caller'],
                'code': context['code']
            }

            deph += 1

        # Parse arguments and assign them to the Block instance
        arguments = getattr(self, 'arguments', {})
        default_arguments = getattr(self, 'defaults', {})
        arguments = parse_arguments(arguments, kwargs, default_arguments)
        for prop, value in arguments.items():
            setattr(self, prop, value)

        # Perform all required building routines
        self.mount(*args, **kwargs)

        # Save the default and passed arguments
        for arg in arguments.keys():
            is_default_argument_method = isinstance(getattr(self, arg), FunctionType)
            is_passed_argument_method = isinstance(kwargs.get(arg, None), FunctionType)

            if hasattr(self, arg) and is_default_argument_method:
                value = getattr(self, arg)(self)
                setattr(self, arg, value)
                value = kwargs[arg](self)
                setattr(self, arg, value)

        self.release()

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

    def mount(self, *args, **kwargs):
        # Last class is object
        classes = getattr(self, 'classes', [])
        classes = classes[:-1]

        # FIXME: Clear builder duplicates
        classes = [cls for cls in classes if 'builder' not in str(cls)]
        # Call .prepare from all inherited classes
        for cls in classes:
            if hasattr(cls, 'prepare'):
                mount_args_keys = getfullargspec(cls.prepare).args
                # TODO: Why we are copy arguments
                mount_kwargs = kwargs.copy()
                if len(mount_args_keys) == 1:
                    args = []

                mount_args = {key: value.copy() if hasattr(value, 'copy') else value for key, value in mount_kwargs.items()
                              if key in mount_args_keys}
                cls.prepare(self, *args, **mount_args)

        self.log(' ; '.join([key + '=' + str(getattr(self, key))
                             for key, value in kwargs.items()]))

    def release(self):
        self.build_frame = {}
        self.build_frames = []

        name = inspect_ref(self)

        self.ref = ref = name

        ref_index = 1
        while self.ref in self.refs:
            self.ref = ref + '_' + str(ref_index)
            ref_index += 1

        self.refs.append(self.ref)

        def tracer(frame, event, arg, self=self):
            if event == 'return':
                self.build_frame = frame
                if frame.f_code.co_name == 'body':
                    self.build_frames.append(frame)

        # tracer is activated on next call, return or exception
        sys.setprofile(tracer)
        tracer_instances.append(tracer)

        try:
            # trace the function
            pass
        finally:
            # disable tracer and replace with old one
            tracer_current = tracer_instances.pop()
            sys.setprofile(tracer_instances[-1])

        self.owner.pop()

        self.log(block_params(self) + '\n')


    def error(self, raise_type, message):
        self.log(message)
        raise raise_type(message)

    def log(self, message, *args):
        # Get the previous frame in the stack, otherwise it would
        # be this function
        func = currentframe().f_back.f_code
        anchor = "[%s:%i:%s] - " % (
            path.basename(path.dirname(func.co_filename)) + '/' + path.basename(func.co_filename),
            func.co_firstlineno,
            func.co_name
        )

        log.info(("%30s" % anchor) + str(self) + ' - ' + str(message), *args)

