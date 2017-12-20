#!/usr/bin/env python

from services.rabbit import MessageQueue

# Sends a HALT message to the first queue in the pipeline. HALT messages are
# propagated to each queue so the entire pipeline should shutdown.
mq = MessageQueue('data')
mq.publish('HALT')