#!/usr/bin/env python

"""Serve medminder state information."""

import os

from flask import Flask

app = Flask(__name__)

@app.route('/')
def root():
    return 'Hello World!'

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT)
