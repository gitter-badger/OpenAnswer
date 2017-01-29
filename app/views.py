from flask import render_template
from app import app

@app.route('/')
def home():
	user = {'nickname': 'Rachel'}  #  fake user
	return render_template('index.html', title='home', user=user)
