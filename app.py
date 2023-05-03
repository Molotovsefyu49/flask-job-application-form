import os
from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Create an app instance using the Flask class

app = Flask(__name__)

# Parameters of the database
load_dotenv()
app.config["SECRET_KEY"] = os.getenv('APP_SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI')
app.config["MAIL_SERVER"] = os.getenv("EMAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("EMAIL_PORT")
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv("EMAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASSWORD")

db = SQLAlchemy(app)

mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


# Render the html home page
@app.route("/", methods=['GET', "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email_address = request.form["email_address"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        form = Form(first_name=first_name, last_name=last_name,
                    email=email_address, date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()

        message_body = f"Thank you for your submission, {first_name}." \
                       f"Here are your data:\n{first_name}\n{last_name}\n{date}" \
                       f"Thank you!"
        message = Message(subject="New form submission",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[email_address],
                          body=message_body)
        mail.send(message)

        flash(f"{first_name}, your form was submitted successfully!", "success")

    return render_template("index.html")


# Execute the web app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)