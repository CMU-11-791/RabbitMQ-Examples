#!/usr/bin/env python

"""
Sends either a HALT or KILL signal (message) to the named queues.
"""
import sys
from services.rabbit import MessageQueue

def kill(name):
    """Send a KILL signal to the named queue.

    KILL signals are not propagated to a Worker's output queue
    """
    print 'Sending KILL to ' + name
    mq = MessageQueue(name)
    mq.publish('KILL')

def halt(name):
    """Send a HALT signal to the named queue.

    HALT signals are not propagated to a Worker's output queue
    """
    print 'Sending HALT to ' + name
    mq = MessageQueue(name)
    mq.publish('HALT')

n = 1
argn = sys.argv[n]
method = kill

if argn == '--halt':
    method = halt
    ++n
elif argn == '--kill':
    method = kill
    ++n

# Any remaining arguments are assumed to be the names of message queues.
for name in sys.argv[n:]:
    if name not in ('data', 'combined', 'sentences', 'tokens', 'tagged', 'my_queue', 'upper'):
        print "Invalid queue name " + name
    else:
        method(name)


