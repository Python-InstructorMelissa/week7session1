from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import image

class User:
    db = 'images'
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.username = data['username']
        self.password = data['password']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.posts = []

    def fullName(self):
        return f'{self.firstName} {self.lastName}'
    
    @staticmethod
    def validate(user):
        isValid = True
        query = 'SELECT * FROM user WHERE username = %(username)s;'
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:
            isValid = False
            flash("That username is already in use")
        if len(user['firstName']) < 2:
            isValid = False
            flash('Please use at least 2 characters for the first name')
        if len(user['lastName']) < 2:
            isValid = False
            flash('Please use at least 2 characters for the last name')
        if len(user['password']) < 8:
            isValid = False
            flash('Password must be at least 8 characters long')
        if user['password'] != user['confirm']:
            isValid = False
            flash('Passwords do not match')
        return isValid

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM user;'
        results = connectToMySQL(cls.db).query_db(query)
        users =[]
        for row in results:
            users.append(cls(row))
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
    def save(cls, data):
        query = 'INSERT INTO user (firstName, lastName, username, password) VALUES (%(firstName)s, %(lastName)s, %(username)s, %(password)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        pass

    @classmethod
    def delete(cls, data):
        pass

    @classmethod
    def getUserImages(cls, data):
        query = 'SELECT * FROM user LEFT JOIN images on user.id = images.user_id WHERE user.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        user = cls(results[0])
        for row in results:
            imageData = {
                'id': row['images.id'],
                'title': row['title'],
                'img': row['img'],
                'info': row['info'],
                'createdAt': row['images.createdAt'],
                'updatedAt': row['images.updatedAt'],
                'user_id': row['user_id'],
            }
            user.posts.append(image.Images(imageData))
        return user
