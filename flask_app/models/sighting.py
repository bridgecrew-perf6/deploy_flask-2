from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import sighting

class Sighting:
    db_name = 'sasquatch_websightings'
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date = data['date']
        self.number = data['number']
        self.reporter_id = data['reporter_id']
        self.reporter_name = data['reporter_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.skeptics = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO sightings (location, description, date, number, reporter_id, reporter_name) VALUES (%(location)s, %(description)s, %(date)s, %(number)s, %(reporter_id)s, %(reporter_name)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        sightings = results[0]
        print(sightings)
        return sightings

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        results = connectToMySQL(cls.db_name).query_db(query)
        sightings = []
        for sighting in results:
            sightings.append(sighting)
        return sightings

    @classmethod
    def update(cls, data):
        query = "UPDATE sightings SET location = %(location)s, description = %(description)s, date = %(date)s, number = %(number)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def number_skeptical(cls, data):
        query = "SELECT * FROM skeptics LEFT JOIN users on skeptics.user_id = users.id WHERE sighting_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        if results == False:
            return 0
        skeptics = []
        for skeptic in results:
            skeptics.append(skeptic)
        print(skeptics)
        return skeptics

    @classmethod
    def skeptical(cls, data):
        query = "INSERT INTO skeptics (user_id, sighting_id) VALUES (%(user_id)s, %(sighting_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def believe(cls, data):
        query = "DELETE FROM skeptics WHERE (user_id, sighting_id) = (%(user_id)s, %(sighting_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def get_user_skeptics(cls, data):
        query = "SELECT * FROM sightings LEFT JOIN skeptics ON skeptics.sighting_id = sightings.id LEFT JOIN users on users.id = skeptics.user_id WHERE sightings.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        skeptical = cls(results[0])
        for row in results:
            if row['users.id'] == None:
                break
            skeptics_data = {
                'id' : row['sightings.id'],
                'location' : row['location'],
                'description' : row['description'],
                'date' : row['date'],
                'number' : row['number'],
                'reporter_id' : row['reporter_id'],
                'reporter_name' : row['reporter_name'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
            }
            skeptical.skeptics.append( sighting.Sighting(skeptics_data))
        return skeptical

    @staticmethod
    def validate_sighting(sighting):
        is_valid = True
        if len(sighting['location']) < 2:
            flash("*Name must contain at least 2 characters!")
            is_valid = False
        if len(sighting['description']) < 10:
            flash("*Description must contain at least 10 characters!")
            is_valid = False
        if len(sighting['date']) == "":
            flash("*Invalid date!")
            is_valid = False
        if len(sighting['number']) < 1:
            flash("*Number sighted must be at least 1!")
            is_valid = False
        return is_valid