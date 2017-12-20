import sys
from rabbit import MessageQueue

mq = MessageQueue('my_queue')
for arg in sys.argv[1:]:
    mq.publish(arg)
