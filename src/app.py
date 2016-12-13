#!/usr/bin/env python3
from flask import Flask, render_template
from time import sleep

def detect_sqli(thing):
	'''
	This doesn't actually detect sqli.
	Please never use this to dectect real sqli.
	The only input came from me during a demo where I knew what it would do if I gave certain inputs.
	'''
	if thing[0] == '\'':
		return True
	if 'or 1=1' in thing:
		return True
	if "SELECT" in thing:
		return True
	return False

def generror(username,password):
	'''
	Generates an error similar (although not identical) to a SQL error message.
	'''
	return "WHERE username='{}' and password ='{}'".format(username,password)

def allow_login(username,password):
	'''
	Determines if the attacker should be sent to the fake admin page.
	The sql injection syntax isn't even correct, but this was meant to be a basic demo.
	'''
	goodu = username in ['aaron','admin','root']
	goodp = password in ["' or 1=1"]
	allow = goodu and goodp
	return allow

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/login')
def sqli():
	'''
	Displays a basic login page.
	The password field isn't obfuscated for demonstration purposes.
	'''
	return render_template('sqli.html')

@app.route('/login/username="<username>"+password="<password>"')
def sqli_result(username,password):
	'''
	This right here is me doing some cool tomfoolery with flask.
	First time I've ever really done anything more interesting than a static webpage.

	Gives a generic fake sql error, checks if you can login, logs you in if you do it right.
	'''
	if all(not detect_sqli(i) for i in [username,password]):
		return render_template('loginfail.html', username=username,password=password)

	if allow_login(username,password):
		return render_template('success.html') #could be a fake admin panel, with more user interactivity
	
	return render_template('fakeinjection.html', error = generror(username,password))


app.run()