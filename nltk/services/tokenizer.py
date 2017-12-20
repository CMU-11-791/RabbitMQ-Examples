from util import timed, parse, as_json
from model import DataSet
from rabbit import Worker
from nltk import word_tokenize


class Tokenizer(Worker):
    """
    The Tokenizer service reads data from the 'sentences' queue, and writes the tokenized
    sentence to the 'tokens' queue.
    """
    def __init__(self, input='sentences', output='tokens'):
        super(Tokenizer,self).__init__('Tokenizer', input, output)

    @timed('Tokenizer')
    def work(self, body):
        data = parse(body, DataSet)
        print "Tokenizing " + data.id
        for s in data.sentences:
            s.tokens = word_tokenize(s.text)

        self.write(as_json(data))


if __name__ == "__main__":
    tokenizer = Tokenizer()
    tokenizer.start()
    print "Tokenizer terminated."
