from flask import Flask, render_template, request

# Create an app instance using the Flask class
app = Flask(__name__)


# Render the html home page
@app.route("/", methods=['GET', "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email_address = request.form["email_address"]
        date = request.form["date"]
        occupation = request.form["occupation"]

    return render_template("index.html")


# Execute the web app
app.run(debug=True, port=5001)