from app import app, db
from app.oauth import OAuthSignIn
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.sql import exists
from .forms import SignupForm
from .models import User


@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=current_user)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/user/<username>')
@login_required
def user(username):
    _user = User.query.filter_by(username=username).first()
    if not _user:
        flash('User %s not found' % username)
        return redirect(url_for('home'))
    posts = []
    return render_template('user.html', user=_user, posts=posts)


@app.route('/signup/<email>', methods=['GET', 'POST'])
def signup(email):
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        if not db.session.query(exists().where(User.username == username)).scalar():
            _user = User(email=email, username=username)
            db.session.add(_user)
            db.session.commit()
            login_user(_user, True)
            return redirect(url_for('home'))
        else:
            form.username.errors.append('That username has been registered, please pick a new one')
    return render_template('signup.html', form=form)


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('home'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('home'))
    oauth = OAuthSignIn.get_provider(provider)
    email = oauth.callback()
    if email is None:
        flash('Authentication failed.')
        return redirect(url_for('home'))
    _user = User.query.filter_by(email=email).first()
    if not _user:
        return redirect(url_for('signup', email=email))
    login_user(_user, True)
    return redirect(url_for('home'))
