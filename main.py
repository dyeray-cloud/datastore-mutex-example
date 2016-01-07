"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from dbmutex import Mutex
import time
app = Flask(__name__)


@app.route('/')
def hello():
    mutex = Mutex()
    start_time = time.time()
    mutex.wait()
    elapsed_time = time.time() - start_time
    time.sleep(2)
    mutex.signal()
    return 'I have waited for %s seconds' % elapsed_time, 200


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
