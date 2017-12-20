# RabbitMQ

[RabbitMQ](https://www.rabbitmq.org) is a light-weight and easy to use [message broker](https://en.wikipedia.org/wiki/Message_broker) that we will use to exchange JSON messages between services.

1. [Introduction]() A quick introduction to RabbitMQ message queues.
1. [NLTK]() A pipeline of NLTK services
1. [Broadcast]() An example of how to blast a message to all listeners.

## Notes

1. RabbitMQ sends messages as byte arrays. These examples assume the byte arrays are UTF-8 strings, but they could be images or video or any other datatype.
1. There is no *Right Way<sup>TM</sup>* to design and build an application using message queues. There may be some [design patterns](https://en.wikipedia.org/wiki/Software_design_pattern) to follow, but RabbitMQ is simply a toolkit for sending messages between processes. What those messages mean and how they are interpreted is up to the producers and consumer of the messages to determine.


