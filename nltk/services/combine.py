from util import timed, parse, as_json
from model import DataSet
from rabbit import Worker

class CombineSnippets(Worker):
    """Combines the text from all the snippets into a single block of text."""

    def __init__(self, input='data', output='combined'):
        super(CombineSnippets,self).__init__('Combine', input, output)

    @timed('Combine')
    def work(self, body):
        terminators = ('.', '!', '?')
        question = parse(body)
        print "Combining snippets for " + question['id']
        snippets = list()
        for snippet in question['snippets']:
            text = snippet['text'].strip()
            if not text.endswith(terminators):
                text = text + '.'
            snippets.append(text)
        data = DataSet()
        data.id = question['id']
        data.text = ' '.join(snippets)
        self.write(as_json(data))


if __name__ == "__main__":
    service = CombineSnippets()
    service.start()
    print "CombineSnippets terminated."
