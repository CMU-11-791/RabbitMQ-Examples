from rabbit import *
import sys

q = MessageQueue('tasks')
b = Broadcaster()

b.broadcast('Starting!')
for i in range(1,20):
    q.publish("T" + str(i))

b.broadcast('Everyone should stop now')

