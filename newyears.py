import os

from flask import Flask
from flask import render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "newyears.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Resolution(db.Model):
  title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

  def __repr__(self):
    return "<Title: {}>".format(self.title)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
  if request.form:
    resolution = Resolution(title=request.form.get("title"))
    db.session.add(resolution)
    db.session.commit()
    print(request.form)
  return render_template("home.html")

if __name__  == "__main__":
  app.run(debug=True)