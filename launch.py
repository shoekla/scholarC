from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
import scrape
import time
import os
app = Flask(__name__)

@app.route('/')
def my_form():
	return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post(ethnicity=None, grade=None,location=None,major=None,startTime=None,timeA=None,gender=None,length=None,links=[]):
	startTime=time.time()
	ethnicity = request.form['ethnicity']
	grade = request.form['grade']
	location = request.form['location']
	major = request.form['major']
	gender = request.form['gender']
	le=scrape.getScholar(ethnicity,grade,location,gender,major)
	links=le
	length=len(links)
	timeA = time.time() - startTime
	return render_template('link.html',ethnicity=ethnicity,grade=grade,location=location,major=major,gender=gender,timeA=timeA,length=length,links=links)

@app.route('/about')
def about():
	return redirect('https://plus.google.com/107108771936096317653/posts')


if __name__ == '__main__':
    app.run()


