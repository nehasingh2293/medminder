#!/usr/bin/env python

"""Serve medminder state information."""

import os

import arrow
from flask import Flask, jsonify
import redis

FIRST_INTERVAL = 0
SECOND_INTERVAL = 30
THIRD_INTERVAL = 45

app = Flask(__name__)
redis_url = os.environ.get('REDISTOGO_URL', 'redis://localhost:6379')
r = redis.from_url(redis_url)

def get_current_time():
    return arrow.now()

def get_interval_end(now):
    """Calculate end time of current interval."""
    first_interval = now.replace(second=FIRST_INTERVAL)
    second_interval = now.replace(second=SECOND_INTERVAL)
    third_interval = now.replace(second=THIRD_INTERVAL)
    if first_interval <= now < second_interval:
        return second_interval
    elif second_interval <= now < third_interval:
        return third_interval
    else:
        return first_interval.replace(minutes=+1)

@app.route('/')
def root():
    return 'Current time: ' + get_current_time().format('dddd HH:mm')

@app.route('/rotate')
def should_rotate():
    """Determine whether pillbox should be rotated."""
    now = get_current_time()
    interval_end_time = arrow.get(r.get('interval_end_time'))

    if now.timestamp < interval_end_time.timestamp:
        return jsonify(should_rotate=False)
    else:
        r.set('interval_end_time', get_interval_end(now))
        return jsonify(should_rotate=True)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    PORT = int(os.environ.get('PORT', 5000))
    r.set('interval_end_time', get_interval_end(get_current_time()))
    app.run(host='0.0.0.0', port=PORT)
