#!/usr/bin/python
import string
import random
import httplib2
import requests
from flask import (
   session as login_session,
   Flask,
   render_template,
   request,
   json,
   jsonify,
   make_response,
   flash
)

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Programs, Courses, Users
from sqlalchemy import create_engine
# Instance of a Flask application
app = Flask(__name__)

# Creating an engine that refer to the database
engine = create_engine('sqlite:///udacity_courses.db')

# Adapting the engine to the metadata of database
Base.metadata.bind = engine

# Create a database session for the engine
session_factory = sessionmaker(bind=engine)
# I used session_factory to avoid threads problem
Session = scoped_session(session_factory)

# The client_id of our google API credentials
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']

# JSON API to show Catalog information (all programs)


@app.route('/catalog/JSON')
@app.route('/programs/JSON')
def jsonify_all_programs():
    session = Session()
    programs = session.query(Programs).all()
    Session.remove()
    return jsonify(
        programs=[program.serialize for program in programs])


# JSON API to show program courses
@app.route('/catalog/<int:program_id>/JSON')
@app.route('/programs/<int:program_id>/JSON')
@app.route('/catalog/<int:program_id>/courses/JSON')
@app.route('/programs/<int:program_id>/courses/JSON')
def jsonify_program(program_id):
    session = Session()
    courses = session.query(Courses).filter_by(program_id=program_id).all()
    Session.remove()
    return jsonify(courses=[course.serialize for course in courses])


# JSON API to show  a specific course information
@app.route('/catalog/<int:program_id>/courses/<int:course_id>/JSON')
@app.route('/programs/<int:program_id>/courses/<int:course_id>/JSON')
def jsonify_course(program_id, course_id):
    session = Session()
    course = session.query(Courses).filter_by(id=course_id).first()
    Session.remove()
    return jsonify(course=[course.serialize])

# Display the root page, we display all disponible porgrams


@app.route('/')
@app.route('/catalog')
@app.route('/programs')
def display_root():
    session = Session()
    # Select all existing programs
    programs = session.query(Programs).all()
    # Select all courses ordered by creation date
    courses = session.query(Courses).order_by(Courses.id.desc())
    # Close the connection
    Session.remove()
    return render_template('all_programs.html',
                           programs=programs, courses=courses)

# Display courses of a specific program


@app.route('/catalog/<string:program_title>')
@app.route('/catalog/<string:program_title>/courses')
@app.route('/programs/<string:program_title>/courses')
def display_program_courses(program_title):
    session = Session()
    # Select all existing programs
    programs = session.query(Programs).all()
    # Select the designed program
    program = session.query(Programs).filter_by(title=program_title).first()
    # Compute how many courses this program has?
    count = session.query(Courses).filter_by(program_id=program.id).count()
    # Select all the courses of this program
    courses = session.query(Courses).filter_by(program_id=program.id).all()
    # Close the connection
    Session.remove()
    return render_template('program_courses.html',
                           programs=programs, courses=courses,
                           programe_title=program.title, count=count)

# Display information of a selected course


@app.route('/catalog/<int:program_id>/<string:course_title>')
@app.route('/programs/<int:program_id>/<string:course_title>')
def display_course_information(program_id, course_title):
    session = Session()
    # Select the designed course
    course = session.query(Courses).filter_by(title=course_title).first()
    # Close the connection
    Session.remove()
    return render_template('course.html', course=course)

# Create a new course after login


@app.route('/catalog/new_course', methods=['GET', 'POST'])
@app.route('/programs/new_course', methods=['GET', 'POST'])
def create_new_course():
    session = Session()
    # Check if the user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'GET':
        # Get all programs
        programs = session.query(Programs).all()

        return render_template('create_new_course.html', programs=programs)
    else:
        # Check if the form was correctly filled in
        if not request.form['title']:
            flash('Enter the course title please!')
            return redirect(url_for('create_new_course'))

        if not request.form['program_id']:
            flash('Select the program of the course please!')
            return redirect(url_for('create_new_course'))

        # Add course
        new_course = Courses(
            title=request.form['title'],
            description=request.form['description'],
            program_id=request.form['program_id'],
            user_id=login_session['user_id'])
        session.add(new_course)
        session.commit()
        # Display the program courses of the new course
        program = session.query(Programs).filter_by(
            id=request.form['program_id']).first()
        Session.remove()
        return redirect(url_for('display_program_courses',
                                program_title=program.title))

# Edit a course created by the current user


@app.route('/catalog/<int:program_id>/<int:course_id>/edit',
           methods=['GET', 'POST'])
@app.route('/programs/<int:program_id>/<int:course_id>/edit',
           methods=['GET', 'POST'])
def edit_course(program_id, course_id):
    session = Session()
    # Check if the user is logged in
    if 'username' not in login_session:
        return redirect('/')
    # Select the targeted course
    course = session.query(Courses).filter_by(id=course_id).first()
    # Check if logged in user is the creator of course
    if course.user_id != login_session['user_id']:
        flash('You are not the author of this course!')
        return redirect('/login')
    if request.method == 'GET':
        # Get all programs
        programs = session.query(Programs).all()
        return render_template('edit_course.html',
                               programs=programs, course=course)
    else:
        # Modify the changed values
        if request.form['title']:
            course.title = request.form['title']
        if request.form['description']:
            course.description = request.form['description']
        if request.form['program_id']:
            course.program_id = request.form['program_id']
        session.add(course)
        session.commit()
        # Session.remove()
        return redirect(url_for('display_course_information',
                                program_id=course.program_id,
                                course_title=course.title))


# Delete a course created by the current user


@app.route('/catalog/<int:program_id>/<int:course_id>/delete',
           methods=['GET', 'POST'])
@app.route('/programs/<int:program_id>/<int:course_id>/delete',
           methods=['GET', 'POST'])
def delete_course(program_id, course_id):
    session = Session()
    # Check if the user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    # Select the targeted course
    course = session.query(Courses).filter_by(id=course_id).first()
    # Check if logged in user is the creator of course
    if course.user_id != login_session['user_id']:
        flash('You are not the author of this course!')
        return redirect('/login')
    if request.method == 'GET':
        return render_template('delete_course.html', course=course)
    else:
        program = session.query(Programs).filter_by(
            id=course.program_id).first()
        session.delete(course)
        session.commit()
        # Session.remove()
        return redirect(url_for('display_program_courses',
                                program_title=program.title))


@app.route('/login')
def login():
    # Create anti-forgery state token
    state = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/logout')
def logout():
    if login_session['provider'] == 'google':
        gdisconnect()
        del login_session['gplus_id']
        del login_session['access_token']

    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['provider']

    return redirect(url_for('display_root'))

# Helper functions in our gconnect function


def create_user(login_session):
    session = Session()
    new_user = Users(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(new_user)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).first()
    Session.remove()
    return user.id


def get_user_id(email):
    session = Session()
    try:
        user = session.query(Users).filter_by(email=email).first()
        Session.remove()
        return user.id
    except:
        Session.remove()
        return None


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token to ensure that the user
    # is making the request and not a malicious code
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code (one-time code)
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        # This line creates an oauth flow object and adds my
        # client's secret key information to it.
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        # Here I specify with post message that this is the
        # one time code flow my server will be sending off.
        oauth_flow.redirect_uri = 'postmessage'
        # I initiate the exchange with the step two exchange
        # function, passing in my one-time code as input.
        credentials = oauth_flow.step2_exchange(code)
    # This step to exchange function of the flow class
    # exchanges an authorization code for a credentials object.
    # If all goes well, then the response from Google will
    # be an object stored in my credentials variable
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid
    access_token = credentials.access_token
    # Google API server can verify if our access_token is valid
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    # Create json GET request containing the url
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        # send internal server error because of invalid access_token
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token doesn't match"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token doesn't match"), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Lastly I will check and see if a user is already logged into the system
    # This will return a 200 successful authentication without resetting
    # all of the login session variables again

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        print('\n user is connected line 192')
        response = make_response(json.dumps('user is connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info from the google server
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # See if user exists
    user_id = get_user_id(data["email"])
    if not user_id:
        user_id = create_user(login_session)
        print('\nCreating a new user')
    login_session['user_id'] = user_id

    return "Login Successful"


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] != '200':
        # If the given token was invalid
        response = make_response(
            json.dumps('Fail to revoke token for given user'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# The app's main
if __name__ == '__main__':
    app.secret_key = 'our_app_secret_key'
    app.debug = True
    host, port = ('localhost', 5000)
    app.run(host=host, port=port)
