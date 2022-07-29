from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models import savedList, note, user

class ListNote:
    db = 'notes'
    def __init__(self, data):
        self.id = data['id']
        self.savedList_id = data['savedList']
        self.note_id = data['note_id']
        self.finalList = []


    @classmethod
    def save(cls, data):
        q = 'INSERT INTO savedList_has_note (savedList_id, note_id) VALUES (%(savedList_id)s, %(note_id)s);'
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def listNotes(cls, data):
        q = 'select * from savedList_has_note left join savedList on savedList.id = savedList_has_note.savedList_id left join note on note.id = savedList_has_note.note_id where savedList_has_note.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(q, data)
        theList = cls(results[0])
        for row in results:
            data = {
                'id': row['savedList.id'],
                'name': row['name'],
                'createdAt': row['savedList.createdAt'],
                'updatedAT': row['savedList.updatedAT'],
                'user_id': row['savedList.user_id'],
            }
            saveList = savedList.SavedList(data)
            data1 = {
                'id': row['note.id'],
                'note': row['note'],
                'createdAt': row['note.createdAt'],
                'updatedAT': row['note.updatedAT'],
                'user_id': row['note.user_id'],
            }
            noteList = note.Note(data1)
            theList.finalList.append(saveList)
            theList.finalList.append(noteList)
            return theList
