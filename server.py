# TODO
# Add a header and footer to the wesbite
# try different color schemes
# Make the python calculator a subpage of the website
# Create a portfolio landing page
#   - It should have an about section
#   - My projects and proficiencies
#   - Emulate a website that I enjoy, like Udemy, youtube, or twitch.
import os
from flask import Flask, render_template, render_template_string, request
import calculator
import flight_messenger

app = Flask(__name__)

email = 'rheckman4143@gmail.com'

calc_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculator')
def calculator_route():
    return render_template('calculator.html')

@app.route('/flights')
def flights_route():
    return render_template('flights.html')

# <div class="response"></div>
@app.route('/flights/submit', methods=['POST'])
def flights_submit():
    if request.method == 'POST':
        phone_number = request.form["phone-number"]
        print(phone_number)
        html_response = """
        <input class="phone" name="phone-number" type="text"/>
        """
        return render_template_string(html_response)
    else:
        return render_template('flights.html')

@app.route('/calculator/submit', methods = ['POST'] )
def calculator_submit():
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
        return render_template('calculator.html')

flight_messenger.start_scheduler()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # Disable debug mode
