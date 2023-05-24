from myapp.hello.models import MESSAGES
from flask import Blueprint

hello = Blueprint('hello', __name__)

@hello.route('/')
@hello.route('/hello')
def hello_world():
    return MESSAGES['default']


@hello.route('/show/<key>')
def get_message(key):
    return MESSAGES.get(key) or "%s not found!" % key


@hello.route('/add/<key>/<message>')
def add_or_update(key, message):
    MESSAGES[key] = message
    return "%s Added/Updated" % key
