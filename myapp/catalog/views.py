from functools import wraps

from flask import request, jsonify, Blueprint, render_template, flash, redirect, url_for
from myapp import db, app
from myapp.catalog.models import Product, Category, ProductForm, CategoryForm

catalog = Blueprint('catalog', __name__)


def template_or_json(template=None):
    def decorated(f):
        @wraps(f)
        def decorated_fn(*args, **kwargs):
            ctx = f(*args, **kwargs)
            if request.is_json or not template:
                return jsonify(ctx)
            else:
                return render_template(template, **ctx)

        return decorated_fn

    return decorated


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@catalog.route('/')
@catalog.route('/katalog')
def home():
    if request.is_json:
        products = Product.query.all()
        return jsonify({
            'count': len(products)
        })
    return render_template('home.html')


@catalog.route('/product/<id>')
def product(id):
    product = Product.query.get_or_404(id)
    return render_template('product.html', product=product)


@catalog.route('/products')
@catalog.route('/products/<int:page>')
def products(page=1):
    products = Product.query.paginate(page=page, max_per_page=3)
    return render_template('products.html', products=products)


@catalog.route('/product-create', methods=['POST', 'GET'])
def create_product():
    form = ProductForm()
    categories = [(c.id, c.name) for c in Category.query.all()]
    form.category.choices = categories

    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        category = Category.query.get_or_404(form.category.data)

        product = Product(name, price, category)
        db.session.add(product)
        db.session.commit()
        flash('The product %s has been created' % name, 'success')
        return redirect(url_for('catalog.product', id=product.id))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('product-create.html', form=form)


@catalog.route('/category-create', methods=['POST', 'GET'])
def create_category():
    form = CategoryForm()

    if request.method == 'POST':
        name = form.name.data
        category = Category(name)
        db.session.add(category)
        db.session.commit()
        flash('The category has been created')
        return redirect(url_for('catalog.category', id=category.id))
    if form.errors:
        flash(form.errors)
    return render_template('category-create.html', form=form)


@catalog.route('/category/<id>')
def category(id):
    category = Category.query.get_or_404(id)
    return render_template('category.html', category=category)


@catalog.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)
