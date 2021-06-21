from datetime import datetime
from flask import render_template
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

