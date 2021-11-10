from app.config.mysqlconnection import connectToMySQL
from flask import flash
from app.models.inventory import Inventory
from app.models.user import User
from app.models.owner import Owner

class OwnerInventory:
    db_name = 'week7_inventory'
    def __init__(self, data):
        self.owner_id = data['owner_id']
        self.inventory_id = data['inventory_id']
        self.count = data['count']
        self.user = None

    @classmethod
    def save(cls, data):
        q = "INSERT INTO owner_has_inventory (owner_id, inventory_id, count) VALUES (%(owner_id)s, %(inventory_id)s, %(count)s);"
        r = connectToMySQL(cls.db_name).query_db(q, data)
        print("print results: ", r)
        return r
        

    @staticmethod
    def validate(inventory):
        isValid = True
        q = "SELECT * FROM owner_has_inventory WHERE  owner_id = %(id)s;"
        r = connectToMySQL(OwnerInventory.db_name).query_db(q, inventory)
        if inventory['inventory_id'] == r['inventory_id']:
            isValid = False
            flash("You already have that item in the list!")
        return isValid