from rabbit import MessageQueue

mq = MessageQueue('my_queue')


def message_handler(channel, method, properties, message):
    if message == 'HALT':
        print("Halting the consumer.")
        mq.stop()
    else:
        print(message)
    mq.ack(method)


mq.register(message_handler)
print("Starting consumer.")
mq.start()
print("Consumer has terminated.")
