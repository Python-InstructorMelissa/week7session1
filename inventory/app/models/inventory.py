from app.config.mysqlconnection import connectToMySQL
from flask import flash
from app.models.user import User
# above brought in the class not just the file
# from app.models import user would bring in the file but later you would have to call user.User

class Inventory:
    db_name = 'week7_inventory'
    def __init__(self, data):
        self.id = data['id']
        self.iName = data['iName']
        self.iImage = data['iImage']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user = None

    @classmethod
    def getAll(cls):
        q = "SELECT * FROM inventory;"
        r = connectToMySQL(cls.db_name).query_db(q)
        inventory = []
        for i in r:
            inventory.append(cls(i))
        return inventory

    @classmethod
    def getOne(cls, data):
        q = "SELECT * FROM inventory WHERE id = %(id)s;"
        r = connectToMySQL(cls.db_name).query_db(q, data)
        return cls(r[0])
    
    @classmethod
    def save(cls, data):
        q = "INSERT INTO inventory (iName, iImage, user_id) VALUES (%(iName)s, %(iImage)s, %(user_id)s)"
        return connectToMySQL(cls.db_name).query_db(q, data)

    @classmethod
    def getOneWithUser(cls, data):
        q = "SELECT * FROM inventory LEFT JOIN user on inventory.user_id = user.id WHERE inventory.id = %(id)s;"
        r =  connectToMySQL(cls.db_name).query_db(q, data)
        print(r)
        data = {"id": r[0]['user.id'], "firstName": r[0]['firstName'], "lastName": r[0]['lastName'], 'username': r[0]['username'], 'uImg': r[0]['uImg'], 'password': r[0]['password'], 'createdAt': r[0]['createdAt'], 'updatedAt': r[0]['updatedAt']}
        inventory=cls(r[0])
        inventory.user=User(data)
        return inventory

        # here because we are only pulling in 1 item due to the way the query is written we don't need to use a for loop to add in the user information but we could use it if we wanted to.