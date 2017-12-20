#!/usr/bin/env python

import threading
from timeit import default_timer as timer

from services.combine import CombineSnippets
from services.splitter import Splitter
from services.tokenizer import Tokenizer
from services.tagger import Tagger
from services.writer import FileWriter
from services.rabbit import MessageQueue
from services.util import parse, as_json

# A list to track all the threads we create.
threads = []

def launch(SeviceClass):
    service = SeviceClass()
    def run():
        service.start()
    t = threading.Thread(target=run)
    t.daemon = True
    threads.append(t)
    t.start()

for service in (CombineSnippets, Splitter, Tokenizer, Tagger, FileWriter):
    launch(service)

with open('data/test.json', 'r') as fp:
    data = parse(fp)

start_time = timer()
mq = MessageQueue('data')
for question in data['questions']:
    mq.publish(as_json(question))

# Send the poison pill down the pipeline
mq.publish('HALT')

# Wait for all the threads to die.
for t in threads:
    t.join()

print "Total time: {:02.6f}s".format(timer() - start_time)
print "DONE"