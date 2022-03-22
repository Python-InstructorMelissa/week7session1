from flask_app.config.mysqlconnection import connectToMySQL
# from flask import flash

class Images:
    db = 'dojogram'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.img = data['img']
        self.info = data['info']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM images;'
        results = connectToMySQL(cls.db).query_db(query)
        imgs = []
        for row in results:
            imgs.append(cls(row))
        return imgs

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM images WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO images (title, img, info, user_id) VALUES (%(title)s, %(img)s, %(info)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE images SET title=%(title)s, img=%(img)s , info-%(info)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM images WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)