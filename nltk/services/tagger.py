from util import timed, parse, as_json
from model import DataSet, Token
from rabbit import Worker
from nltk import pos_tag


class Tagger(Worker):
    """Run nltk.pos_tag"""
    def __init__(self):
        super(Tagger,self).__init__('Tagger', 'tokens', 'tagged')

    @timed('Tagger')
    def work(self, body):
        data = parse(body, DataSet)
        print "Tagging " + data.id
        for sent in data.sentences:
            tokens = [ t.word for t in sent.tokens ]
            sent.tokens = [Token(t[0],t[1]) for t in pos_tag(tokens)]
        self.write(as_json(data))


if __name__ == "__main__":
    service = Tagger()
    service.start()
    print "POS Tagger terminated."