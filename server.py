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
