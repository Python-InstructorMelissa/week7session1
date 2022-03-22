from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/', methods=['POST'])
def register():
    isValid = User.validate(request.form)
    if not isValid:  # if isValid = False then redirect to /
        return redirect('/')
    newUser = {
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'username': request.form['username'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(newUser)
    if not id:
        flash('Something went wrong')
        return redirect('/')
    session['user_id'] = id
    flash("You are now logged in")
    return redirect('/dashboard/')

@app.route('/login/', methods=['POST'])
def login():
    data = {
        'username': request.form['username']
    }
    user = User.getUsername(data) # check if the email is in the database
    if not user: # if not let them know
        flash('That username is not in our database please register')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Wrong password')
        return redirect('/')
    session['user_id'] = user.id
    flash("You are now logged in")
    return redirect('/dashboard/')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

