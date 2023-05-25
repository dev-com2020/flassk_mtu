import ccy as ccy
from flask import Flask, request
from myapp.hello.views import hello
from flask_sqlalchemy import SQLAlchemy
from myapp.product.views import product_blueprint


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

db = SQLAlchemy(app)


from myapp.catalog.views import catalog

app.register_blueprint(hello)
app.register_blueprint(product_blueprint)
app.register_blueprint(catalog)


@app.template_filter('format_currency')
def format_currency_filter(amount):
    currency_code = ccy.countryccy(request.accept_languages.best[-2:]) or 'USD'
    return '{0} {1}'.format(currency_code, amount)


# https://github.com/dev-com2020/flassk_mtu

