#!/usr/bin/env bash

pip install pika
pip install nltk

python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
