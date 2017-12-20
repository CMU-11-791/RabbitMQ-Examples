# RabbitMQ

[RabbitMQ](https://www.rabbitmq.org) is a light weight message broker that enables communication between processes, even if those processes are running in different programs or on different machines.

## Prerequisites

1. The Pika Python package.
    ```
    $> pip install pika
    ```
1. [Docker](https://docs.docker.com/engine/installation/) to run the RabbitMQ server.


### Starting The RabbitMQ Server

Fortunately RabbitMQ is distributed as a Docker image so once you have [Docker installed](https://docs.docker.com/engine/installation/) no other setup is required.

```
$> docker run -d -p 5672:5672 -p 15672:15672 --hostname deiis --name rabbit rabbitmq:3-management
```

After the RabbitMQ server has started (give it a minute or two) you can view the management console at [http://localhost:15672](http://localhost:15672) (username:*guest*, password:*guest*). You can use the management console to inspect and purge the message queues when needed during development and testing, but it will not be used in this tutorial.


# RabbitMQ 101

In RabbitMQ there are message `exchanges` and message `queues`. To send a message you send it to an `exchange`. To receive messages you create a `queue` and attach it to an `exchange`.

![Exchange to Queue](https://www.rabbitmq.com/img/tutorials/python-three-overall.png)

Here the producer **P** sends messages to the exchange **X** and two consumers; **C<sub>1</sub>** and **C<sub>2</sub>** have attached queues to the exchange.  How RabbitMQ distributes the messages depends on the `exchange` type.

There are four exchange types:

1. **Work Queue**: Messages are distributed in a round robin fashion to the registered consumers. This is the default type of exchange created.
1. **Broadcast**: Messages are distributed to all registered consumers.
1. **Direct**: Messages are dispatched to consumers based on an id (a *routing key* in RabbitMQ-speak).
1. **Topic** Like a *Direct* exchange except wildcards can be used in the *routing key*.

See the [RabbitMQ Getting Started page](https://www.rabbitmq.com/getstarted.html) for more details.

# Message Queues

In this tutorial we will create a simple producer/consumer workflow using the `MessageQueue` class defined in the `rabbit.py` file. The `MessageQueue` class encapsulates a RabbitMQ *work queue* exchange and handles the mundane tasks required to setup a message queue. The `MessageQueue` class provides four methods:

1. **publish(string)** sends the message to the exchange.
1. **register(callback)** registers the `callback` function as a consumer of the message queue.  RabbitMQ will invoke the *callback* funtion when messages arrive on the queue.
1. **start()** start waiting for messages to appear on the queue.
1. **stop()** disconnects a consumer from a queue.

## The Producer

The `producer.py` script reads command line arguments and publishes each argument to an exchange named *my_queue*.

```python
import sys
from rabbit import MessageQueue

mq = MessageQueue('my_queue')

for arg in sys.argv[1:]:
    mq.publish(arg)

```

**NOTE** We do not need to do anything other than declare a `MessageQueue` instance and provide the name of a queue, and we can make up as many names as we need/want.  If a message queue with that name doesn't exist RabbitMQ will create it for us.

## The Consumer: Take One

The `consumer1.py` script registers a `message_handler` method for the *my_queue* message queue. RabbitMQ will call the `message_handler` method every time a message appears on the queue.

```python
from rabbit import MessageQueue

mq = MessageQueue('my_queue')

def message_handler(channel, method, properties, message):
    print(message)

mq.register(message_handler)
print "Starting consumer."
mq.start()
print "Consumer has terminated."
```

Note that `MessageQueue.start()` is a *blocking* method, that is, it will not return until another thread kills it. More on that below.

### Running The Example

Open two shell (terminal) windows. Launch the `consumer1.py` script in the first window and run the `producer.py` script in the second window.

```
# Shell 1
$> python consumer1.py

# Shell 2
$> python producer.py Hello world
```

You should see the strings *Hello* and *world* printed in the consumer's window.

Now press `Ctrl+C` in the consumer window to kill the consumer script and re-run it.  You should see:

```
$> python consumer1.py
Staring consumer.
Hello
world
```

What happened?  Why was *Hello* and *world* printed again? Didn't we already consume those messages?

The problem is that our consumer did not *acknowledge* that it had successfully processed each message.  If a consumer dies before it acknowledges a message, because of an exception or it was killed with `Ctrl+C`, RabbitMQ will reissue those messages to new consumers that become available.  If you open [http://localhost:15672](http://localhost:15672) in your browser you should see that the *my_queue* message queue still contains two unacknowledged messages.

## The Consumer : Take Two

The `consumer2.py` fixes this problem by calling the `mq.ack(method)` to *ack*nowledge that the messages have been successfully processed.

```python
def message_handler(channel, method, properties, message):
    print(message)
    mq.ack(method)
```

When you run the `consumer2.py` script it will print the *Hello world* messages again (provided you haven't removed the messages with the management console).  However, if you kill the `consumer2.py` script and re-run it the *Hello world* messages should be gone and no more output is produced until you queue up more messages with the `producer.py` script.

However, there is still a problem: using `Ctrl+C` is not a good way to kill a consumer as it may be in the middle of processing a message and/or the consumer may need to perform some cleanup before exiting; e.g. closing database connections, ensuring disk caches are flushed, etc.

## The Consumer : Take Three

The `consumer3.py` script addresses the above problem by using a *poison pill*, which is simply a fixed known message that the consumer recognizes as a signal that it is supposed to shut down.  We will use the string *HALT* as our poison pill.

```python
def message_handler(channel, method, properties, message):
    if message == 'HALT':
        print "Halting the consumer."
        mq.stop()
    else:
        print(message)
    mq.ack(method)
```

Now if we publish a *HALT* message the consumer will shutdown cleanly.

```
$> python producer.py Hello world HALT
$> python consumer3.py
Starting consumer.
Hello
world
Halting the consumer.
Consumer has terminated.
$>
```

Notice:

1. We run the `producer.py` script first to pre-populate the message queue for the consumer. We have seen that RabbitMQ will hold messages until something consumes them so this is safe to do. We also queue up the HALT message at the same time.
1. The HALT message itself it not printed, although we could change the consumer to do so if we wanted.
1. We see the "Consumer has terminated." message for the first time!  This means the call to `mq.start()` has exited cleanly.

# Work Flows

A common design pattern when implementing work flows is to have a message queue between each pair of processes.

```
 DATA -> Q1 -> P1 -> Q2 -> P2 -> ... -> Qn -> Pn
```

The `rabbit.py` file defines the classes `Consumer` and `Worker` for implementing a workflow like the above. The `Consumer` class maintains an input queue and registers its `work` method to receive messages that arrive on the queue.  The `Worker` class extends `Consumer`, but also manages an output queue and provides a `write` method for writing to the output queue.

The `workflow.py` script implements a simple work flow consisting of two processes. The first process is a `Worker` that converts incoming messages to uppercase and writes them to its output queue.  The second process is a consumer and prints incoming messges.

```python
from rabbit import Consumer, Worker

class ToUpper(Worker):
    def __init__(self, name='ToUpper'):
        super(ToUpper, self).__init__(name, 'my_queue', 'upper')

    def work(self, message):
        self.write(message.upper())

class Printer(Consumer):
    def __init__(self, name='Printer'):
        super(Printer, self).__init__(name, 'upper')

    def work(self, message):
        print message
```

The `workflow.py` scripts runs the two processes in separate threads using the Python `threading` module.  Once again we will run the `producer.py` script first to pre-populate the queue with data, including the *poison pill*.

```
$> python producer.py hello world HALT
$> python workflow.py
Printer starting
ToUpper starting
HELLO
WORLD
Halting worker ToUpper
ToUpper halted.
Halting consumer Printer
Printer halted.
```

# Scaling The Work Flow

So far we have used one instance for each of our services. While this works if all services run in approximately the same amount of time, in practice it is likely that some services take much longer to complete their tasks that others.

To simulate this case we will introduce `time.sleep()` calls to our `work` methods so that the `ToUpper` class produces elements twice as fast as the `Printer` class can consume them.

```python
class ToUpper(Worker):
    ...
    def work(self, message):
        print self.name + ": " + message
        time.sleep(1)
        self.write(message.upper())

class Printer(Consumer):
    ...
    def work(self, message):
        time.sleep(2)
        print self.name + ': ' + message

```

To compensate for the differences in processing times we will launch two instances of the `Printer` service. This is referred to as [horizontal scaling](https://en.wikipedia.org/wiki/Scalability#Horizontal_and_vertical_scaling).

```python
launch(Printer, 'P1')
launch(Printer, 'P2')
launch(ToUpper, 'T1')
```

Now that we have to `Printer` services running they should be able to keep up with the `ToUpper` service. The `workflow2.py` script launches two instances of the `Printer` service and one instance of the `ToUpper` service.

```
$> python producer.py goodbye cruel world I am leaving you today
$> python workflow2.py
P1 starting
P2 starting
T1 starting
T1: goodbye
T1: cruel
T1: world
P1: GOODBYE
T1: I
P2: CRUEL
T1: am
P1: WORLD
T1: leaving
T1: you
P2: I
P1: AM
T1: today
P2: LEAVING
P1: YOU
P2: TODAY
```

Notice that P1 and P2 take turns handling messages.

# Final Notes

Unfortunately the strategy of using a *poison pill* to shutdown the workflow is not as straight-forward when multiple consumers are listening to a message queue. For example, running `python producer.py HALT` does not cause the `workflow2.py` script to terminate since only one of the `Printer` instances will receive the *HALT* message, leaving the other thread running.

There are a number of possible solutions to the above problem, two common approaches are:

1. Keep track of the number of consumers for each message queue and place that number of poison pills on the message queue.
1. Have a [broadcast](https://www.rabbitmq.com/tutorials/tutorial-three-python.html) message queue, that is, a queue that delivers a message to all of its subscribed consumers rather than dealing messages out to just one consumer.

Solving the above problem is left as an exercise for the reader.  However, in the meantime you can kill the *hung* `workflow2.py` script by putting another `HALT` message on the *upper* message queue that the final `Printer` thread is waiting on:

```
$> python -c "from rabbit import MessageQueue; MessageQueue('upper').publish('HALT')"
```

Of course, you can always use the `ps` command to get the pid (process id) of the running script and use the `kill` command to forcefully close the program.
