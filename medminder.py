#!/usr/bin/env python

"""Serve medminder state information."""

import os

import arrow
from flask import Flask
import redis

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_current_time():
    return arrow.now()

@app.route('/')
def root():
    return 'Current time: ' + get_current_time().format('dddd HH:mm')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT)
