# RabbitMQ Example

This example extends the ideas presented in the [first example](https://github.com/CMU-11-791/RabbitMQ-Examples/tree/master/intro) to run a work flow of NLTK services (sentence spitter, tokenizer, and part of speech tagger) on a sample BioASQ data file. We will also have a service that combines the text for all snippets into a single string, and an *output* service that writes files to disk. 

| Service | Description |
|---|---|
| **combine.py** | Combines the text for all snippets into a single string |
| **splitter.py** | Runs the NLTK sentence splitter |
| **tokenizer.py** | Runs sentences through the NLTK tokenizer |
| **tagger.py** | Runs the NLTK part of speech tagger |
| **writer.py** | Writes each file to the /tmp directory |

## Contents

- [Running The Examples](#running_the_example)
- [Design Notes](#design_notes)

## Prerequisites

1. The Python packages NLTK and Pika
1. [Docker](https://docs.docker.com/engine/installation/) to run the RabbitMQ server.

```
$> pip install nltk
$> pip install pika
$> python -c "import nltk; nltk.download('punkt')"
```

Users with a Bash shell can use the *init.sh* script to install and configure the required packages.

### Starting The RabbitMQ Server

Fortunately RabbitMQ is distributed as a Docker image so once you have [Docker installed](https://docs.docker.com/engine/installation/) no other setup is required.

```
$> docker run -d -p 5672:5672 -p 15672:15672 --hostname deiis --name rabbit rabbitmq:3-management
```

After the RabbitMQ server has started you can view the management console at [http://localhost:15672](http://localhost:15672) (username:*guest*, password:*guest*). You can use the management console to inspect and purge the message queues when needed.


## Running The Example

There are two ways to run the services in parallel; using Python Threads or running each service program in its own shell. In either case the code for the services is exactly the same.

### Python Threads

The `threaded.py` script runs each service in a Python thread. 

```
$> python threaded.py
```

One of Python's biggest drawbacks is that it is single threaded. The `threading` package provides some relief, but there is still the GIL (Global Interpreter Lock) to deal with.

### Separate Shells

Running each service in its own shell is almost twice as fast as using Python threads as now the operating system can utilize all available cores, something Python is not able to do on its own.  This approach also closely resembles running each service in its own Docker container.

Three Python scripts are provided to run the complete example:

1. **start.py** Starts all of the Python scripts (services) in separate shells so they run in parallel.
1. **pipeline.py** Reads the `data/test.json` file and publishes each question to the *data* queue.
1. **halt.py** Kills the pipeline

```
$> python start.py
$> python pipeline.py
$> python halt.py
```

> **NOTE** The `start.py` script launches each service in a background shell, so all of the services echo output to the same parent shell window.  If it looks like the program has *hung* it just means some service(s) have output something causing the prompt that was displayed to scroll up.  Just hit the ENTER key to get your prompt back.
>
> Alternatively, run the `start.py` script in one window and the `pipeline.py` and `halt.py` scripts in another window.


