from decimal import Decimal

from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import StringField, DecimalField, SelectField, TextAreaField
from wtforms.validators import InputRequired, NumberRange
from wtforms.widgets import Select, html_params

from myapp import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('products', lazy='dynamic'))

    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def __repr__(self):
        return '<Product %d>' % self.id


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %d>' % self.id


class NameForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])




class CustomCategoryInput(Select):
    def __call__(self, field, **kwargs):
        html = []
        for val, label, selected in field.iter_choices():
            html.append(
                '<input type="radio" %s> %s' % (html_params(
                    name=field.name, value=val, checked=selected, **kwargs), label
                ))
            return Markup(''.join(html))


class CategoryField(SelectField):
    widget = CustomCategoryInput()

    def iter_choices(self):
        categories = [(c.id, c.name) for c in Category.query.all()]
        for value, label in categories:
            yield (value, label, self.coerce(value) == self.data)

    def pre_validate(self, form):
        for v, _ in [(c.id, c.name) for c in Category.query.all()]:
            if self.data == v:
                break
            else:
                raise ValueError(self.gettext('Not a valid choice'))


class ProductForm(NameForm):
    price = DecimalField('Price', validators=[InputRequired(), NumberRange(min=Decimal('0.0'))])
    category = CategoryField('Category', coerce=int, validators=[InputRequired()])


class CategoryForm(NameForm):
    name = TextAreaField('Name', validators=[InputRequired()])
