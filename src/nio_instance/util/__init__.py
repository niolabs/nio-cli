""" Some utility functions and constants for the instance CLI

"""
import re
from .config_property import ConfigProperty
from .execution import Execution


LIST_FORMAT = "http://{0}:{1}/{2}/{3}"
COMMAND_FORMAT = "http://{0}:{1}/services/{2}/{3}/"
SHUTDOWN = "http://{0}:{1}/shutdown"


def try_int(arg):
    result = arg
    try:
        result = int(arg)
    except:
        pass
    return result

def try_bool(arg):
    result = arg
    if re.match(r'[fF]', arg):
        result = False
    elif re.match(r'[tT]', arg):
        result = True
    return result

def argument(s):
    try:
        terms = s.split('=')
        terms[1] = try_int(terms[1])
        
        # # there's no boolean command param right now
        # terms[1] = try_bool(terms[1])
    except:
        raise ArgumentTypeError(
            "Command arguments must be of form 'foo=bar'"
        )
    return terms

def edge(s):
    try:
        frm, to = s.split('=>')
        to = to or None
        return [frm, to]
    except:
        raise ArgumentTypeError(
            "Link arguments must be of the form 'foo=>bar'"
        )
