from flask_app.config.mysqlconnection import connectToMySQL
# from flask import flash

class Images:
    db = 'dojogram'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.images_id = data['images_id']
        self.comment = data['comment']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM interaction;'
        results = connectToMySQL(cls.db).query_db(query)
        interactions = []
        for row in results:
            interactions.append(cls(row))
        return interactions

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM interaction WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO interaction (images_id, user_id, comment) VALUES (%(images_id)s, %(user_id)s, %(comment)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE interaction SET comment=%(comment)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM interaction WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)