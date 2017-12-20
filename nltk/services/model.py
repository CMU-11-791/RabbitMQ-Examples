"""Classes for the data model as well as a JSONEncoder to write them as JSON."""
# import json
#
#
# class Encoder(json.JSONEncoder):
#     def default(self, obj):
#         if type(obj) in (Sentence, Token, DataSet):
#             return obj.__dict__
#         # if isinstance(obj, Sentence) or isinstance(obj, Token) or isinstance(obj, DataSet):
#         #     return obj.__dict__
#         else:
#             return json.JSONEncoder.default(self, obj)
#
#
# def as_json(obj):
#     return json.dumps(obj, cls=Encoder, indent=4)


class DataSet(object):
    """DataSet instances maintain the list of sentences for a paragraph."""
    def __init__(self, arg=None):
        if arg is not None:
            self.id = arg['id']
            self.text = arg['text']
            self.sentences = [ Sentence(s) for s in arg['sentences']]
        else:
            self.id = False
            self.text = ''
            self.sentences = []

    def add(self, sentence):
        self.sentences.append(sentence)


class Sentence(object):
    """Sentences maintain the list of Tokens in a sentence."""
    def __init__(self, arg=None):
        if arg is None:
            return
        elif isinstance(arg, dict):
            self.text = arg['text']
            if 'tokens' in arg:
                self.tokens = [Token(t) for t in arg['tokens']]
            else:
                self.tokens = []
        else:
            self.text = arg
            self.tokens = []


class Token(object):
    """A Token consists of the word and an optional part of speech tag."""
    def __init__(self, arg=None, pos=None):
        if arg is None:
            return

        if isinstance(arg, dict):
            self.word = arg['word']
            if 'pos' in arg:
                self.pos = arg['pos']
            else:
                self.pos = False
        else:
            self.word = arg
            if pos is None:
                self.pos = False
            else:
                self.pos = pos

