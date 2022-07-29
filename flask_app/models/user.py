from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models.savedList import SavedList

class User:
    db='notes'
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.username = data['username']
        self.email = data['email']
        self.level = data['level']
        self.adminKey = data['adminKey']
        self.password = data['password']
        self.lists = []

    @staticmethod
    def validate(u):
        isValid = True
        q = 'SELECT * FROM user WHERE username = %(username)s;'
        r = connectToMySQL(User.db).query_db(q, u)
        if len(r) >= 1:
            isValid = False
            flash("That username is already being used")
        if u['password'] != u['confirm']:
            isValid = False
            flash("Your Passwords don't match")
        return isValid

    @classmethod
    def save(cls, data):
        q = 'INSERT INTO user (firstName, lastName, username, email, password) VALUES (%(firstName)s, %(lastName)s, %(username)s,%(email)s,%(password)s);'
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def getAll(cls):
        q = 'SELECT * FROM user;'
        r = connectToMySQL(cls.db).query_db(q)
        users = []
        for user in r:
            users.append(cls(user))
        return users

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getUsername(cls, data):
        query = "SELECT * FROM user WHERE username = %(username)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update(cls, data):
        q = 'UPDATE user SET level=%(level)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def usersLists(cls, data):
        q = 'SELECT * FROM user LEFT JOIN note on note.user_id = user.id WHERE user.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(q, data)
        theList = cls(results[0])
        for row in results:
            data = {
                'id': row['note.id'],
                'name': row['name'],
                'createdAt': row['createdAt'],
                'updatedAT': row['updatedAT'],
                'user_id': row['user_id']
            }
            list = SavedList(data)
            theList.lists.append(list)
            return theList