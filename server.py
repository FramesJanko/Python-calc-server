# TODO
# Add a header and footer to the wesbite
# try different color schemes
# Make the python calculator a subpage of the website
# Create a portfolio landing page
#   - It should have an about section
#   - My projects and proficiencies
#   - Emulate a website that I enjoy, like Udemy, youtube, or twitch.
from flask import Flask, render_template, render_template_string, request
import calculator

app = Flask(__name__)

email = 'rheckman4143@gmail.com'

calc_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculator')
def calculator_route():
    return render_template('calculator.html')

@app.route('/calculator/submit', methods = ['POST'] )
def submit():
    if request.method == 'POST':
        calculation = calculator.calculate(request.form["calculation"])
        calc_history.append(calculation)
        html_response = """
        <div class ="response">
            <div class="answer">{{ calculation }}</div>
            <div class="history">
                <ul>
                {% for item in calc_history %}
                    <li>{{ item }}</li>
                {% endfor %}
                </ul>
            </div>
        </div>
        """
        return render_template_string(html_response, calculation=calculation, calc_history=calc_history)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
