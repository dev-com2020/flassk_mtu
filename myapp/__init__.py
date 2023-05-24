from flask import Flask, Blueprint
from myapp.hello.views import hello

# bp = Blueprint('example',__name__)

app = Flask(__name__)
app.register_blueprint(hello)
__all__ = []