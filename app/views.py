from flask import render_template, flash, redirect, url_for
from app import app, db
from .models import User
from flask_login import login_user, logout_user, current_user, login_required
from app.oauth import OAuthSignIn


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
        # TODO: Prompt them to choose a username
        username = email.split('@')[0]
        _user = User(email=email, username=username)
        db.session.add(_user)
        db.session.commit()
    login_user(_user, True)
    return redirect(url_for('home'))
