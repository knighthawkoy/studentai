# UI Interface for Flask API using JINJA Templates #
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add your authentication logic here
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

