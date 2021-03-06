"""
this is a simple app for illustrating CRUD in flask
you shall learn about the program structure of flask in one of the future tutorials.
"""
# importing necessary models
import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from flask_migrate import Migrate

# creating the initial configurations
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = "This can be any thing"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "database.db")
db = SQLAlchemy(app)
Migrate(app, db)


# creating the database model

class Puppies(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name, self.id}"


# creating the form fields

class PuppiesForm(FlaskForm):
    name = StringField("Name:")
    submit = SubmitField("Add")
    update = SubmitField("Update")


# creating creating views
# view for adding item to database
@app.route('/', methods=['GET', 'POST'])
def index():
    form = PuppiesForm()
    if form.validate_on_submit():
        new_puppy = Puppies(name=form.name.data)
        db.session.add(new_puppy)
        db.session.commit()
        return redirect(url_for("list"))
    return render_template('add.html', form=form)


# view for listing items on the database
@app.route("/ list of puppies", methods=['GET', 'POST'])
def list():
    puppies = Puppies.query.all()
    form = PuppiesForm()
    return render_template('list.html', puppies=puppies, form=form)


# view for updating data in the database
@app.route("/ update puppies record <_id>", methods=['GET', 'POST'])
def update(_id):
    puppy = Puppies.query.filter_by(id=_id).first()
    form = PuppiesForm(name=puppy.name)
    if form.validate_on_submit():
        Puppies.query.filter_by(id=_id).update({"name":form.name.data})
        db.session.commit()
        return redirect(url_for("list"))
    return render_template("update.html", form=form)


# view for deleting record from the database
@app.route("/delete <_id>")
def delete(_id):
    puppy = Puppies.query.filter_by(id=_id).first()
    db.session.delete(puppy)
    db.session.commit()
    return redirect(url_for("list"))


# view for deleting all records on the database
@app.route("/delete all ")
def delete_all():
    puppies = Puppies.query.all()
    for puppy in puppies:
        db.session.delete(puppy)
    db.session.commit()
    return redirect(url_for("list"))


if __name__ == "__main__":
    app.run(debug=True)
