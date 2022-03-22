from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_app.models.image import Images
from flask_app.models.user import User

@app.route('/dashboard/')
def dashboard():
    if 'user_id' not in session:
        flash('Hey there log in first dude!!!')
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    theUser = User.getOne(data)
    userPosts = User.getUserImages(data)
    return render_template('dashboard.html', user=theUser, posts=userPosts)

@app.route('/dojoGram/add/')
def addDojoGram():
    if 'user_id' not in session:
        flash('Hey there log in first dude!!!')
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    theUser = User.getOne(data)
    return render_template('addDojoGram.html', user=theUser)

@app.route('/dojoGram/create/', methods=['POST'])
def createDojoGram():
    data = {
        'title': request.form['title'],
        'img': request.form['img'],
        'info': request.form['info'],
        'user_id': request.form['user_id'],
    }
    Images.save(data)
    return redirect('/dashboard/')

@app.route('/dojoGram/<int:id>/view/')
def viewDojoGram(id):
    if 'user_id' not in session:
        flash('Hey there log in first dude!!!')
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    imgId = {
        'id': id
    }
    theUser = User.getOne(data)
    theDojoGram = Images.getOne(imgId)
    return render_template('viewDojoGram.html', user=theUser, image=theDojoGram)

@app.route('/dojoGram/feed/')
def feed():
    if 'user_id' not in session:
        flash('Hey there log in first dude!!!')
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    theUser = User.getOne(data)
    theUsers = User.getAll()
    allPosts = Images.getAll()
    return render_template('feed.html', user=theUser, users=theUsers, posts=allPosts)