from app import app
from flask import Flask, render_template, redirect, session, request, flash
import re
from  flask_bcrypt import Bcrypt
from app.models.user import User
from app.models.inventory import Inventory
from app.models.owner import Owner

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('home.html', user=User.getOne(data), items=Inventory.getAll())

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=User.getOne(data), ownerList=Owner.getOwners(data))

@app.route('/addInventory')
def addInventory():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('addInventory.html', user=User.getOne(data))

@app.route('/createInventory', methods=['POST'])
def createInventory():
    data = {
        'iName': request.form['iName'],
        'iImage': request.form['iImage'],
        'user_id': request.form['user_id']
    }
    Inventory.save(data)
    return redirect('/home')

@app.route('/createList', methods=['POST'])
def createList():
    data = {
        'oList': request.form['oList'],
        'user_id': request.form['user_id']
    }
    Owner.save(data)
    return redirect('/dashboard')

@app.route('/user/viewUser/<int:id>')
def viewUser(id):
    data = {
        'id': id
    }
    return render_template('viewProfile.html', user=User.getOne(data))

@app.route('/user/updateUser/<int:id>')
def updateUser(id):
    data = {
        'id': id
    }
    return render_template('updateUser.html', user=User.getOne(data))

@app.route('/user/editUser/<int:id>', methods=['POST'])
def editUser(id):
    data = {
        'id': id,
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'uImg': request.form['uImg']
    }
    User.update(data)
    return redirect('/dashboard')

@app.route('/item/<int:id>')
def viewItem(id):
    data = {
        'id': id
    }
    print("Single Item: ", Inventory.getOne(data))
    return render_template('viewItem.html', item=Inventory.getOneWithUser(data), user=User.getAll())