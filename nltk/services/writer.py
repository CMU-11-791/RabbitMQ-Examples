
from util import timed, parse, as_json
from model import DataSet
from rabbit import Consumer

class FileWriter(Consumer):
    """
    The FileWriter reads from the 'tagged' queue and writes the tokens to a
    file in the /tmp directory. The packet (question) id is used as the file name.
    """
    def __init__(self):
        super(FileWriter, self).__init__('Writer', 'tagged')

    @timed('Writer')
    def work(self, body):
        data = parse(body, DataSet)
        path = '/tmp/' + data.id + '.json'
        with open(path, 'w') as fp:
            fp.write(as_json(data))
            print 'Wrote ' + path


if __name__ == "__main__":
    service = FileWriter()
    service.start()
    print "FileWriter terminated."
