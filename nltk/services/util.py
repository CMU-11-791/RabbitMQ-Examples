import json
from timeit import default_timer as timer
from functools import wraps
from model import *

def timed(name):
    """A decorator to record the running time of a function."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            start = timer()
            result = fn(*args, **kwargs)
            elapsed = timer() - start
            print '{} {:02.6f}s'.format(name, elapsed)
            return result
        return wrapper
    return decorator


class Encoder(json.JSONEncoder):
    """Allow our data model classes to be serialized to JSON."""
    def default(self, obj):
        if type(obj) in (Sentence, Token, DataSet):
            return obj.__dict__
        else:
            return json.JSONEncoder.default(self, obj)


def as_json(obj):
    """Always use the as_json() method to ensure the proper encoder is used."""
    return json.dumps(obj, cls=Encoder, indent=4)


def parse(input, Class=None):
    """Parses the input JSON string.

    If the Class is specified we attempt to create an instance.
    """
    if isinstance(input, file):
        obj = json.load(input)
    else:
        obj = json.loads(input)
    if Class is not None:
        obj = Class(obj)
    return obj


