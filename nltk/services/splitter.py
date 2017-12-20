from util import timed, parse, as_json
from model import DataSet, Sentence
from nltk import sent_tokenize
from rabbit import Worker


class Splitter(Worker):
    """Runs the NLTK sentence splitter."""

    def __init__(self):
        super(Splitter,self).__init__('Splitter', 'combined', 'sentences')

    @timed('Splitter')
    def work(self, body):
        data = parse(body, DataSet)
        print "Splitting " + data.id
        sentences = sent_tokenize(data.text)
        for s in sentences:
            data.sentences.append(Sentence(s))

        self.write(as_json(data))


if __name__ == "__main__":
    splitter = Splitter()
    splitter.start()
    print 'Splitter terminated'

