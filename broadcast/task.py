from rabbit import *
import threading
import sys

class Task(object):
    def __init__(self, name):
        self.name = name
        self.input = MessageQueue('tasks')
        self.input.register(self.handle_message)
        self.listener = BroadcastListener()
        self.listener.register(self.handle_broadcast)
        self.thread = False

    def handle_broadcast(self, channel, method, properties, message):
        print(self.name + " BROADCAST: " + message)
        if message == 'DIE':
            self.input.stop()
            self.listener.stop()

    def handle_message(self, channel, method, properties, message):
        print(self.name + " MESSAGE: " + message)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        print("Starting " + self.name)

        def start_listening():
            try:
                self.listener.start()
            except Exception as e:
                print(e)

        self.thead = threading.Thread(target=start_listening)
        self.thead.daemon = True
        self.thead.start()
        self.input.start()
        print("Waiting for our thread to die...")
        self.thead.join()

if __name__ == "__main__":
    task = Task(sys.argv[1])
    task.start()
