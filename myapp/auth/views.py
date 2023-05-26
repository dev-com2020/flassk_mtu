from flask import Blueprint, render_template, session, flash, redirect, url_for, request, g
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from myapp import db, app
from myapp.auth.models import RegistrationForm, User, LoginForm

auth = Blueprint('auth', __name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.before_request
def get_current_user():
    g.user = current_user

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
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    form = LoginForm()

    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        existing_username = User.query.filter_by(username=username).first()

        if not (existing_username and existing_username.check_password(password)):
            flash("Niepoprawne dane logowanie")
            return render_template('login.html', form=form)

        login_user(existing_username)

        return redirect(url_for('auth.home'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Jesteś wylogowany")
    return redirect(url_for('auth.home'))
