from rabbit import MessageQueue

mq = MessageQueue('my_queue')


def message_handler(channel, method, properties, message):
    print(message)


mq.register(message_handler)
print("Starting consumer.")
mq.start()
print("Consumer has terminated.")
