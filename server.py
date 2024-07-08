# TODO
# Add a header and footer to the wesbite
# try different color schemes
# Make the python calculator a subpage of the website
# Create a portfolio landing page
#   - It should have an about section
#   - My projects and proficiencies
#   - Emulate a website that I enjoy, like Udemy, youtube, or twitch.
from flask import Flask, render_template, request
import calculator

app = Flask(__name__)

email = 'rheckman4143@gmail.com'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods = ['POST'] )
def submit():
    if request.method == 'POST':
        calculation = calculator.calculate(request.form["calculation"])
        return (f'<div class="answer">{calculation}</div>')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
