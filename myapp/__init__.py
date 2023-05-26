import ccy as ccy
from flask import Flask, request
from myapp.hello.views import hello
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.secret_key = 'some_random_key'
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
app.config['LDAP_PROVIDER_URL'] = 'ldap://localhost'

db = SQLAlchemy(app)

from myapp.catalog.views import catalog
from myapp.auth.views import auth

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# def get_ldap_connection():
    # conn = ldap.initialize(app.config['LDAP_PROVIDER_URL'])
    # return conn


app.register_blueprint(hello)
app.register_blueprint(catalog)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()


@app.template_filter('format_currency')
def format_currency_filter(amount):
    currency_code = ccy.countryccy(request.accept_languages.best[-2:]) or 'USD'
    return '{0} {1}'.format(currency_code, amount)

# https://github.com/dev-com2020/flassk_mtu
