from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, session

from poll import app

@app.route('/')
@app.route('/home')
def home():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    return render_template(
        "index.html",
        title="Welcome there", 
        message="this is a message",
        content="on "+formatted_now)

@app.route('/api/data')
def get_data():
  return app.send_static_file('data.json')


@app.route('/login')
def login():
  if request.method == "POST":
  
    key = request.form['secret_key']

    flash('Thanks')

    return redirect(url_for('home'))
  
  # get request, just render the template
  return render_template('login.html')
