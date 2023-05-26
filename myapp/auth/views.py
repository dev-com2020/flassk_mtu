from flask import Blueprint, render_template, session, flash, redirect, url_for, request

from myapp import db
from myapp.auth.models import RegistrationForm, User, LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/')
@auth.route('/home')
def home():
    return render_template('home.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('username'):
        flash('Już jesteś zalogowany', 'info')
        return redirect(url_for('auth.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash("Nazwa użytkownika już istnieje")
            return render_template('register.html', form=form)
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        flash("Możesz się już zalogować")
        return redirect(url_for('auth.login'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        existing_username = User.query.filter_by(username=username).first()
        if not (existing_username and existing_username.check_password(password)):
            flash("Niepoprawne dane logowanie")
            return render_template('login.html', form=form)
        session['username'] = username
        return redirect(url_for('auth.home'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        flash("Jesteś wylogowany")
    return redirect(url_for('auth.home'))
