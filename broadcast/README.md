# Broadcast Queue

This is a short example of using a broadcast (fanout) exchange/queue to send message to multiple listeners at once.

## Running The Example

Launch multiple instances of the `task.py` script.  Each time the `task.py` script is invoked it will run an instances of the `Task` class in its own thread.

```bash
$> python task.py P1 &
$> python task.py P2 &
$> python task.py P3 &
$> python task.py P4 &

```

Run the `main.py` script to send messages to the running tasks.

```
$> pythong main.py
P3 BROADCAST: Starting!
P2 BROADCAST: Starting!
P1 BROADCAST: Starting!
P4 BROADCAST: Starting!
P1 MESSAGE: T1
P1 MESSAGE: T5
P2 MESSAGE: T2
P3 MESSAGE: T3
P4 MESSAGE: T4
P2 MESSAGE: T6
P3 MESSAGE: T7
P1 MESSAGE: T9
P4 MESSAGE: T8
P3 MESSAGE: T11
P2 MESSAGE: T10
P4 MESSAGE: T12
P1 MESSAGE: T13
P2 MESSAGE: T14
P4 MESSAGE: T16
P1 MESSAGE: T17
P2 MESSAGE: T18
P4 BROADCAST: Everyone should stop now
P2 BROADCAST: Everyone should stop now
P1 BROADCAST: Everyone should stop now
P3 MESSAGE: T15
P3 BROADCAST: Everyone should stop now
P3 MESSAGE: T19
```
Run the `kill.py` script to send a *poison pill* to the running tasks.

```
$> python kill.py
P1 BROADCAST: DIE
P2 BROADCAST: DIE
P3 BROADCAST: DIE
P4 BROADCAST: DIE
Waiting for our thread to die...
Waiting for our thread to die...
Waiting for our thread to die...
Waiting for our thread to die...
```