from flask import render_template, flash, redirect, url_for
from app import app, db
from .models import User
from flask_login import login_user, logout_user, current_user, login_required
from .oauth import OAuthSignIn


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
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User %s not found' % username)
        return redirect(url_for('home'))
    posts = []
    return render_template('user.html', user=user, posts=posts)


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
    user = User.query.filter_by(email=email).first()
    if not user:
        # TODO: Prompt them to choose a username
        username = email.split('@')[0]
        user = User(email=email, username=username)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('home'))
