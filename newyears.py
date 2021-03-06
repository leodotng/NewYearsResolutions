import os

from flask import Flask
from flask import redirect
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

@app.route("/", methods=["GET", "POST"])
def home():
    resolutions = None
    if request.form:
      try:
          resolution = Resolution(title=request.form.get("title"))
          db.session.add(resolution)
          db.session.commit()
      except Exception as e:
          print("Failed to add Resolution")
          print(e)
    resolutions = Resolution.query.all()
    return render_template("home.html", resolutions=resolutions)

@app.route("/update", methods=["POST"])
def update():
    try: 
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        resolution = Resolution.query.filter_by(title=oldtitle).first()
        resolution.title = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update Resolution!")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    resolution = Resolution.query.filter_by(title=title).first()
    db.session.delete(resolution)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
  app.run(debug=True)