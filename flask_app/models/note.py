from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Note:
    db='notes'
    def __init__(self, data):
        self.id = data['id']
        self.note = data['note']
        self.private = data['private']
        self.user_id = data['user_id']

    @classmethod
    def getAll(cls):
        q = 'SELECT * FROM note;'
        r = connectToMySQL(cls.db).query_db(q)
        notes = []
        for note in r:
            notes.append(cls(note))
        return notes

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM note WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        q = 'INSERT INTO note (note, private, user_id) VALUES (%(note)s, %(private)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def update(cls, data):
        q = 'UPDATE note SET note=%(note)s, private=%(private)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def delete(cls, data):
        q = 'DELETE FROM note WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(q, data)