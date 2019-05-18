#!/usr/bin/python
from flask import render_template
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Programs, Courses, Users
from sqlalchemy import create_engine
from flask import Flask
# Instance of a Flask application
app = Flask(__name__)

# Creating an engine that refer to the database
engine = create_engine('sqlite:///udacity_courses.db')

# Adapting the engine to the metadata of database
Base.metadata.bind = engine

# Create a database session for the engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Show the root page, we display all disponible porgrams
@app.route('/')
@app.route('/programs')
def showRoot():
    programs = session.query(Programs).all()
    return render_template('all_programs.html', programs=programs)

# Show courses of a specific program
@app.route()


# The app's main
if __name__ == '__main__':
    app.secret_key = 'our_app_secret_key'
    app.debug = False
    host, port = ('localhost', 5000)
    app.run(host=host, port=port)
