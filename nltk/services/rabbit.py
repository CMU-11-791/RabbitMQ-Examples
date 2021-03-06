import pika
from timeit import default_timer as timer

PERSIST = pika.BasicProperties(delivery_mode=2)

class MessageQueue:
    """
    The MessageQueue class provides some simple helper methods to manage RabbitMQ
     message queues.
    """
    def __init__(self, name, host='localhost', exchange='', durable=False, fair=False):
        self.exchange = exchange
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(name, durable=durable)
        # Set fair=True if multiple consumers are reading from a single queue.
        if fair:
            self.channel.basic_qos(prefetch_count=1)
        self.queue = name

    def publish(self, message):
        """Published the message to the queue managed by this instance."""
        self.channel.basic_publish(self.exchange, routing_key=self.queue, body=message, properties=PERSIST)

    def register(self, handler):
        """Registers the handler as a consumer for the queue managed by this instance."""
        self.tag = self.channel.basic_consume(handler, self.queue)

    def start(self):
        """Start waiting for messages to arrive on our queue."""
        self.channel.start_consuming()

    def stop(self):
        self.channel.basic_cancel(self.tag)

    # @classmethod
    def ack(self, method):
        self.channel.basic_ack(delivery_tag=method.delivery_tag)


class Consumer(object):
    """
    A Consumer receives messages from an input queue and "consumes" them.

    What is meant by "consume" depends on what subclasses do in their `work`
    methods.  However, Consumers do not produce "output" in the sense
    that they do not write to an output queue.
    """

    def __init__(self, name, input):
        self.name = name
        self.input_queue = MessageQueue(input)
        self.input_queue.register(handler=self._handler)

    def _handler(self, channel, method, properties, body):
        """RabbitMQ will call the _handler method when a message arrives on the queue."""
        if body == 'HALT':
            self.input_queue.stop()
            # Allow Workers to propagate the HALT message to their output_queue.
            self.halt()
        elif body == 'KILL':
            # Stops the input queue but does not propagate the messaes any further.
            self.input_queue.stop()
        elif body == 'TIMER_START':
            self.start_time = timer()
        elif body == 'TIMER_STOP':
            self.stop_timer(self.start_time)
        elif body.startswith('TIMER_STOP '):
            start_time = body.split()[1]
            self.stop_timer(start_time)
        else:
            self.work(body)

        # Acknowledge that the message was processed.
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def work(self, body):
        """Subclasses will override the work method to perform their work"""
        pass

    def halt(self):
        """Overloaded by the Worker class to propagate HALT messages."""
        print "Halting consumer " + self.name

    def stop_timer(self, start_time):
        elapsed = timer() - float(start_time)
        print "Total elapsed time: {:02.6f}s".format(elapsed)

    def start(self):
        """Start listening on our input_queue.

        MessageQueues are blocking so the start() method will block until another
        process cancels the queue by sending a HALT message
        """
        print self.name + " starting"
        self.input_queue.start()
        print self.name + " halted."

'''
Workers are like Consumers except they write to an output queue.
'''
class Worker(Consumer):
    def __init__(self, name, input, output):
        super(Worker, self).__init__(name, input)
        self.output_queue = MessageQueue(output)

    def write(self, message):
        self.output_queue.publish(message)

    def halt(self):
        self.output_queue.publish('HALT')
        print "Halting worker " + self.name

    def stop_timer(self, start_time):
        self.write('TIMER_STOP ' + str(start_time))
