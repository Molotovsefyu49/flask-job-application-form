from flask import Flask, render_template

# Create an app instance using the Flask class
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

# Execute the web app
app.run(debug=True, port=5001)