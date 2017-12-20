#!/usr/bin/env python

# NOTE
# Before running the pipeline.py script you must first run the start.py script
# to launch all the services.  Use the halt.py script to kill the services
# when you are done.

from services.util import parse, as_json
from services.rabbit import MessageQueue

# The first message queue in the pipeline.
q = MessageQueue('data')

with open('data/test.json', 'r') as fp:
    data = parse(fp)

q.publish('TIMER_START')
for question in data['questions']:
    q.publish(as_json(question))
q.publish('TIMER_STOP')
print "pipeline.py done."