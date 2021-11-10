from app.config.mysqlconnection import connectToMySQL
from flask import flash
from app.models.user import User
# above brought in the class not just the file
# from app.models import user would bring in the file but later you would have to call user.User

class Owner:
    db_name = 'week7_inventory'
    def __init__(self, data):
        self.id = data['id']
        self.oList = data['oList']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user = None
        self.inList = []

    @classmethod
    def getAll(cls):
        q = "SELECT * FROM owner;"
        r = connectToMySQL(cls.db_name).query_db(q)
        owner = []
        for i in r:
            owner.append(cls(i))
        return owner

    @classmethod
    def getOne(cls, data):
        q = "SELECT * FROM owner WHERE id = %(id)s;"
        r = connectToMySQL(cls.db_name).query_db(q, data)
        return cls(r[0])

    @classmethod
    def getOwners(cls, data):
        q = "SELECT * FROM owner WHERE user_id = %(id)s;"
        r = connectToMySQL(cls.db_name).query_db(q, data)
        print("All owner results: ", r)
        iList = []
        for i in r:
            iList.append(cls(i))
            print("iList in loop: ", iList)
        print("iList after loop: ", iList)
        return iList
    
    @classmethod
    def save(cls, data):
        q = "INSERT INTO owner (oList, user_id) VALUES (%(oList)s, %(user_id)s)"
        return connectToMySQL(cls.db_name).query_db(q, data)

    @classmethod
    def getOneWithUser(cls, data):
        q = "SELECT * FROM owner LEFT JOIN user on owner.user_id = user.id WHERE owner.id = %(id)s;"
        r =  connectToMySQL(cls.db_name).query_db(q, data)
        print(r)
        data = {"id": r[0]['user.id'], "firstName": r[0]['firstName'], "lastName": r[0]['lastName'], 'username': r[0]['username'], 'uImg': r[0]['uImg'], 'password': r[0]['password'], 'createdAt': r[0]['createdAt'], 'updatedAt': r[0]['updatedAt']}
        owner=cls(r[0])
        owner.user=User(data)
        return owner

        # here because we are only pulling in 1 item due to the way the query is written we don't need to use a for loop to add in the user information but we could use it if we wanted to.


        

