import logging
from collections import deque
from .args import get_params


def logger_init(name, filename='bem.log'):
    logging.setLoggerClass(logging.Logger)
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    log_handler = logging.FileHandler(filename)

    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    log.addHandler(log_handler)

    return log


# ERC Logger grabber
class TailLogHandler(logging.Handler):
    def __init__(self, log_queue):
        logging.Handler.__init__(self)
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.append(self.format(record))


class TailLogger(object):
    def __init__(self, maxlen):
        self._log_queue = deque(maxlen=maxlen)
        self._log_handler = TailLogHandler(self._log_queue)

    def contents(self):
        return '\n'.join(self._log_queue)

    @property
    def log_handler(self):
        return self._log_handler


def ERC_logger():
    erc = logging.getLogger('ERC_Logger')
    tail = TailLogger(10)
    log_handler = tail.log_handler
    for handler in erc.handlers[:]:
        erc.removeHandler(handler)

    erc.addHandler(log_handler)

    return tail


def SKIDL_logger():
    erc = logging.getLogger('skidl')
    tail = TailLogger(10)
    log_handler = tail.log_handler
    for handler in erc.handlers[:]:
        erc.removeHandler(handler)

    erc.addHandler(log_handler)

    return tail


def block_definition(block, args, kwargs):
    # Aggregate block definition for logging
    definition = []
    def print_value(value):
        if isinstance(value, list):
           return ' '.join(value)
        else:
           return str(value)

    mods = ' ; '.join([key + '=' + print_value(value) for key, value in block.mods.items()])
    props = ' ; '.join([key + '=' + print_value(value) for key, value in block.props.items()])
    args = ' ; '.join([key + '=' + str(value) for key, value in kwargs.items()])
    # models = ', '.join([str(model) for model in block.models])
    # classes = ', '.join([str(model) for model in block.classes])

    if mods:
        definition.append(mods)

    if props:
        definition.append(props)

    if args:
        definition.append(args)

    # if models:
    #    definition.append(models)

    # if classes:
    #    definition.append(classes)

    return ' | '.join(definition)

def block_params(block):
    def print_value(value):
        if hasattr(value, 'suffix'):
            return str(value['value']) + ' ' + value['unit'].get('suffix', '')
        else:
            return str(value['value']).replace(':', '/')

    params = get_params(block)

    return ' ; '.join([key + '=' + print_value(value) for key, value in params.items()])
