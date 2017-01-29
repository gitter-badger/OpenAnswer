from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/')
def home():
	user = {'nickname': 'Rachel'}  #  fake user
	posts = [ # fake array of posts
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

@app.route('/login', methods=['GET', 'POST'])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		flash(
			'Login requested for OpenID=%s, remember_me=%s' % 
			(form.openid.data, str(form.remember_me.data))
		)
	return render_template(
		'login.html',
		title='Sign in',
		form=form
	)
