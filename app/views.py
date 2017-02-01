from flask import render_template, flash, redirect, url_for
from app import app, db
from .forms import LoginForm
from .models import User
from flask_login import login_user, logout_user, current_user
from .oauth import OAuthSignIn


@app.route('/')
def home():
    user = {'nickname': 'User'}  # fake user
    posts = [  # fake array of posts
        {
            'author': user,
            'body': 'Teach me web dev please.'
        },
        {
            'author': user,
            'body': 'I\'m not sure I\'m sober'
        },
    ]
    return render_template(
        'index.html', title='home', user=user, posts=posts
    )


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash(
#             'Login requested for OpenID=%s, remember_me=%s' %
#             (form.openid.data, str(form.remember_me.data)))
#         return redirect('/')
#     return render_template(
#         'login.html',
#         title='Sign in',
#         form=form,
#         providers=app.config['OPENID_PROVIDERS']
#     )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))

