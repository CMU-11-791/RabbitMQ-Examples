import os
from services.model import  timed
from nltk import sent_tokenize, word_tokenize, pos_tag

text = 'Goodbye cruel world. I am leaving you today. Goodbye (3 times).'
value = os.environ.get("FOO")
if value is None:
	print 'FOO was not set.'

@timed("Serial")
def run():
	for s in sent_tokenize(text):
		tokens = word_tokenize(s)
		for token in pos_tag(tokens):
			print token

run()


