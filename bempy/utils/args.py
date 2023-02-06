import json
from copy import copy
from inspect import getfullargspec, getmembers, isroutine
from inspect import signature as func_signature

from . import uniq_f7
from .parser import block_params_description


def value_to_strict(value):
    default = value
    # if type(value) in [UnitValue, PeriodValue, FrequencyValue]:
    #     value = {
    #         'value': default.value * default.scale,
    #         'unit': {
    #             'name': default.unit.unit_name,
    #             'suffix': default.unit.unit_suffix
    #         }
    #     }
    # el
    if type(default) in [int, float]:
        value = {
            'value': default,
            'unit': {
                'name': 'number'
            }
        }
    elif type(default) == str:
        value = {
            'value': default,
            'unit': {
                'name': 'string'
            }
        }
    elif type(default) == type(None):
        value = {
            'unit': {
                'name': 'network'
            }
        }
    else:
        return False

    return value


def value_to_round(value):
    is_ci_value = False # isinstance(value, (UnitValue, PeriodValue, FrequencyValue))

    if is_ci_value:
        value = value.canonise() if value.value else value
        value = {
            'value': round(value.value, 1),
            'unit': {
                'name': value.unit.unit_name,
                'suffix': value.prefixed_unit.str()
            }
        }
    elif isinstance(value, (int, float)):
        value = {
            'value': value if isinstance(value, int) else round(value, 3),
            'unit': {
                'name': 'number'
            }
        }
    elif isinstance(value, str):
        value = {
            'value': value,
            'unit': {
                'name': 'string'
            }
        }
    else:
        return False


    return value


def default_arguments(block):
    args = []
    defaults = {}

    classes = block.classes
    classes.reverse()
    for cls in classes:
        if hasattr(cls, 'init'):
            args += getfullargspec(cls.init).args
            signature = func_signature(cls.init)
            defaults = { **defaults,
                     **{
                        k: v.default
                        for k, v in signature.parameters.items()
                    }
            }

    args = uniq_f7([arg for arg in args if arg != 'self'])

    return args, defaults


def get_arguments(block):
    arguments = {}

    description = block_params_description(block)
    def_arguments, defaults = default_arguments(block)

    for arg in getattr(block, 'arguments', {}):
        default = getattr(block, arg, defaults.get(arg, None))
        is_list = arg == 'Load' and isinstance(default, list) and len(default)

        if is_list:
            default = default[0]

        value = value_to_strict(default)
        if value:
            arguments[arg] = value
        if description.get(arg, None) and arguments.get(arg, None):
            arguments[arg]['description'] = description[arg]

    return arguments


def get_params(block):
    params = {}
    params_default = getmembers(block, lambda a: not (isroutine(a)))

    description = block_params_description(block)

    params = {}
    arguments = getattr(block, 'arguments', [])
    black_list = ['name', '__module__'] + arguments
    for param, default in params_default:
        # Skip unrelated attributes
        # TODO: make faster check
        if param.startswith('_') \
                or param in black_list:
            continue

        value = value_to_round(default)

        if value:
            params[param] = value

        if description.get(param, None) and params.get(param, None):
            params[param]['description'] = description[param]

    return params


def parse_arguments(arguments, request, defaults):
    props = {}

    for attr in arguments:
        value = request.get(attr, None)

        props[attr] = copy(defaults.get(attr, None)) #copy(getattr(cls, attr))

        if isinstance(value, type(None)):
            continue

        if isinstance(value, dict):
            value = value.get('value', value)

        #if isinstance(props[attr], bool):
        #    props[attr] = value
        if isinstance(props[attr], (int, float)):
            props[attr] = float(value)
        #elif type(props[attr]) in [str, bool]:
        #    props[attr] = arg
        # elif type(props[attr]) == list:
        #    props[attr] = props[attr][0]
        # elif isinstance(props[attr], (UnitValue, PeriodValue, FrequencyValue)):
        #     if isinstance(value, (UnitValue, PeriodValue, FrequencyValue)):
        #         # unit value
        #         props[attr] = value
        #     elif isinstance(value, slice):
        #         # slice(start, stop, step)
        #         props[attr]._value = value.stop
        #     elif isinstance(value, list):
        #         # Range [start, stop]
        #         props[attr]._value = value[1]
        #     else:
        #         # number
        #         props[attr]._value = float(value)
        else:
            props[attr] = value

    return props


def descript_params(block, params):
    params['params'] = {param: params['params'][param]
                        for param in params['params'].keys() if not params['args'].get(param, None)}

    description = block_params_description(block)
    for param in description.keys():
        if params['args'].get(param, None):
            params['args'][param]['description'] = description[param]

        if params['params'].get(param, None):
            params['params'][param]['description'] = description[param]

    return params


def has_attr_value(block, attr, key, value):
    if value in getattr(block, attr).get(key, []):
        return True

    return False


def has_prop(block, prop, value):
    return has_attr_value(block, 'props', prop, value)


def has_mod(block, mod, value):
    return has_attr_value(block, 'mods', mod, value)

def safe_serialize(obj):
  default = lambda o: str(o)
  return json.dumps(obj, default=default)

def cached_property(func):
    " Used on methods to convert them to methods that replace themselves\
        with their return value once they are called. "

    def cache(*args):
        self = args[0] # Reference to the class who owns the method
        funcname = func.__name__
        ret_value = func(self)
        setattr(self, funcname, ret_value) # Replace the function with its value
        return ret_value # Return the result of the function

    return property(cache)
