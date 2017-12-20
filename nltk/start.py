#!/usr/bin/env python

"""Run all of the services used in the pipeline."""
import os

# dir = os.environ.get('PYMEDTERMINO_DATA_DIR')
# if dir is None:
#     print "Please set PYMEDTERMINO_DATA_DIR before starting the services."
#     exit(1)

for name in ['combine', 'splitter', 'tokenizer', 'tagger', 'writer']:
    os.system("python services/{}.py &".format(name))

print "The services have been started."
