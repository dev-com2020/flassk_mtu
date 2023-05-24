import ccy as ccy
from flask import Flask, request
from myapp.hello.views import hello

# bp = Blueprint('example',__name__)
from myapp.product.views import product_blueprint

app = Flask(__name__)
app.register_blueprint(hello)
app.register_blueprint(product_blueprint)


def format_currency_filter(amount):
    currency_code = ccy.countryccy(request.accept_languages.best[-2:]) or 'USD'
    return '{0} {1}'.format(currency_code, amount)

# __all__ = []

# https://github.com/dev-com2020/flassk_mtu
