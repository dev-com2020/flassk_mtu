from flask import Flask
from myapp import app

# print(flask.__version__)

# app = Flask(__name__)
# app.config.from_pyfile('setup.ini')
# app.config.from_object('config.ProductionConfig')
# app.config['DEBUG'] = True

#
# @app.route('/')
# def hello():
#     return '<img src="/static/images/kruk.jpeg">'
app.debug = 'development'
app.run()
