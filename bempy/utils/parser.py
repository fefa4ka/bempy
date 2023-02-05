from inspect import getsourcelines, getouterframes, linecache
import builtins
import re
from functools import reduce
from sys import _getframe as getframe
import inspect, sys



def inspect_code(instance, frame):
    ref = None
    context = {
        'caller': None,
        'code': '',
        'ref': ref
    }
    frame_locals = frame.f_locals

    local_self = frame_locals.get('self', None)

    if local_self != instance:
        ref = frame_locals
        for key, value in frame_locals.items():
            if isinstance(instance, type(value)) and instance == value:
                ref = key
                break

        try:
            # FIXME: Detect source of execution
            cell_code = linecache.getlines(inspect.getfile(frame))
            code = cell_code
            code = getsourcelines(frame)[0]

            code_line = frame.f_lineno - frame.f_code.co_firstlineno
        except OSError:
            # If code runned from shell
            # maybe code available global
            context = {
                'caller': None,
                'code': getattr(builtins, 'code', ''),
                'ref': ref
            }

            if not hasattr(builtins, 'code'):
                return context

            code = builtins.code.split('\n')
            code_line = frame.f_lineno - 1

        context = {
            'caller': frame_locals.get('self', None),
            'source': code,
            'code': code[code_line] if len(code) > code_line else '',
            'ref': ref
        }

        comment_line_start = comment_line_end = code_line

        parentheses_open_pos = context['code'].find('(')
        parentheses_close_pos = context['code'].find(')')

        # In code there aren't method call, lookup code for local variable
        code_part = [line.replace(' ', '') for line in code[0:code_line]]
        code_part.reverse()

        if parentheses_open_pos == -1 or (context['code'].find('=') == -1 and parentheses_open_pos > parentheses_close_pos):
            local_vars = frame.f_code.co_varnames[1:]

            for index, line in enumerate(code_part):
                parentheses_open_pos = line.find('(')
                parentheses_close_pos = line.find(')')

                # Block constructed from local method
                if line.find('return') == 0:
                    context['ref'] = None
                    break

                # Block assigned as local variable
                for var in local_vars:
                    if var + '=' in line:
                        context['code'] = line
                        comment_line_start = code_line - index

                        break
                else:
                    continue

                break
            else:
                context['code'] = ''

        elif context['code'].find('=') == -1 or context['code'].find('return') != -1:
            for index, line in enumerate(code_part):
                if line.find('def') == 0:
                    comment_line_start = code_line - index
                    context['code'] = line[3:line.find('(')] + '=()'
                    break

        context['comment_line_start'] = comment_line_start
        context['comment_line_end'] = comment_line_end

    return context


def inspect_comments(code, start, end):
    notes = []

    if start > len(code):
        return []

    if start > 0 and code[start - 1].strip() == '"""':
        new_end = start
        start -= 1
        while start > 0 and code[start - 1].strip() != '"""':
            start -= 1

        note = []
        for line_number in range(start, new_end - 1):
            line = code[line_number]
            note.append(line.strip())

        notes.append('\n'.join(note))

        start = new_end

    while start > 0 and code[start - 1].strip().find('#') == 0:
        start -= 1

    for line_number in range(start, end + 1):
        line = code[line_number]
        has_comment = line.find('#')
        if has_comment != -1:
            comment = line[has_comment + 1:].strip()
            if comment:
                notes.append(comment)

    notes.reverse()

    return notes


def trace_call_comment(depth=1):
    frame = getframe(depth)
    if frame.f_code.co_name != 'circuit':
        frame = getframe(depth + 1)

    # Search in code
    code = []
    notes = []
    try:
        code = getsourcelines(frame.f_code)[0]
        code_line = frame.f_lineno - frame.f_code.co_firstlineno
    except OSError:
        if hasattr(builtins, 'code'):
            code = builtins.code.split('\n')
            code_line = frame.f_lineno - 1

    if len(code):
        notes = inspect_comments(code, code_line, code_line)

    return notes


def inspect_ref(block):
    """
    Ref extracted from code variable name
    """
    origin_ref = ref = getattr(block, 'ref', '')
    name: str = ref or getattr(block, 'name', '')
    name = name.split('.')[-1]

    context = block.context
    code = context['code']
    caller = context['caller']

    assign_pos = code.find('=')
    and_pos = code.find('&')
    or_pos = code.find('|')
    parentheses_pos = code.find('(')
    ref = code[:assign_pos].strip().replace('self', '')
    ref = re.sub("[\(\[].*?[\)\]]", "", ref)
    ref = re.sub('[(){}<>]', '', ref)
    ref = ref.strip().capitalize()
    value = code[assign_pos:]
    ref = ''.join([word.capitalize() for word
                   in ref.replace('_', '.').split('.')])

    if parentheses_pos > 0 and assign_pos > parentheses_pos:
        ref = name

    if assign_pos == -1 or code.find('return') != -1 or (and_pos != -1 and assign_pos > and_pos) or (or_pos != -1 and assign_pos > or_pos) or value == code:
        ref = name

    if caller and hasattr(caller, 'name') and not hasattr(caller, 'root'):
        block_name = caller.ref.split('.')[-1]
        #if block_name not in ref:
        short_name = ''.join(re.findall('[A-Z]+', block_name))
        ref = short_name + '_' + ref

    def short_tokens(origin_ref, length=-1):
        tokens = re.findall('[A-Z0-9][^A-Z0-9]*', origin_ref)
        short_name = ''.join([token[0:length] for token in tokens])
        return short_name

    return ref

    refs = [short_tokens(ref)]
    if origin_ref:
        short_name = short_tokens(origin_ref)
        refs.append(short_name)

    total_ref = '_'.join(refs)

    return total_ref

    if len(ref) > 7:
        total_ref = total_ref.replace('_', '')

    if len(total_ref) > 7:
        total_ref = short_tokens(total_ref)

    if len(ref) > 7:
        total_ref = ''.join(re.findall('[A-Z0-9]+', total_ref))

    return total_ref

    # FIXME: Make a better

    if len(ref) > 7:
        total_ref = total_ref.replace('_', '')

    if len(total_ref) > 7:
        total_ref = short_tokens(total_ref)

    if len(total_ref) > 7:
        total_ref = short_tokens(total_ref, 3)

    if len(total_ref) > 7:
        total_ref = short_tokens(total_ref, 2)

    if len(total_ref) > 7:
        total_ref = ''.join(re.findall('[A-Z0-9]+', total_ref))

    return total_ref


def block_ref(block):
    if not hasattr(block, 'part') and block:
        return block.ref
    else:
        return getattr(block, 'ref', '') + ' / ' + str(block)


def block_description(block):
    """
    From docsting of classes builded from.
    """
    description = []
    for doc in [cls.__doc__ for cls in block.classes if cls.__doc__ and cls != object]:
        doc = '\n'.join([line.strip() for line in doc.split('\n')])
        description.append(doc)

    return description


def block_params_description(block):
    """
    Get documentation from docstring of methods in `self.doc_methods`
    using pattern 'some_arg -- description'
    """
    def extract_doc(cls):
        doc = ''

        if cls == object:
            return doc

        for method in block.doc_methods:
            doc_str = hasattr(cls, method) and getattr(cls, method).__doc__
            if doc_str:
                doc += doc_str

        return doc

    params = {}

    docs = [extract_doc(cls) for cls in block.classes]

    for doc in docs:
        terms = [line.strip().split(' -- ') for line in doc.split('\n')
                 if len(line.strip())]

        for term, description in terms:
            params[term.strip()] = description.strip()

    return params


def deep_get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
                  keys.split("."),
                  dictionary)

