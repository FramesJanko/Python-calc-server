from flask import Flask, render_template

app = Flask(__name__)

variable = 'test'
email = 'rheckman4143@gmail.com'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ContactMe')
def contact():
    return f'<h1>Contact Me at {email}</h1>'

if __name__ == '__main__':
    app.run(debug=True)
