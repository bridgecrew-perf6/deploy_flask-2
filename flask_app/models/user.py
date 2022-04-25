from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    db_name = 'sasquatch_websightings'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.sightings = []
        
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def one_user_info(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        user_info = cls(results[0])
        return user_info

    # @classmethod
    # def get_user_paintings(cls, data):
    #     query = "SELECT * FROM users LEFT JOIN owners ON owners.user_id = users.id LEFT JOIN paintings on paintings.id = owners.painting_id WHERE users.id = %(id)s;"
    #     results = connectToMySQL(cls.db_name).query_db(query, data)
    #     user_paintings = cls(results[0])
    #     for row in results:
    #         if row['paintings.id'] == None:
    #             break
    #         painting_data = {
    #             'id' : row['paintings.id'],
    #             'title' : row['title'],
    #             'description' : row['description'],
    #             'price' : row['price'],
    #             'quantity' : row['quantity'],
    #             'artist_id' : row['artist_id'],
    #             'created_at' : row['created_at'],
    #             'updated_at' : row['updated_at']
    #         }
    #         user_paintings.paintings.append( painting.Painting(painting_data))  
    #     return user_paintings

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @staticmethod
    def validate_user(user):
        is_valid = True
        fname = str(user['first_name'])
        lname = str(user['last_name'])
        user_in_db = User.get_by_email({'email': user['email']})
        if len(user['first_name']) < 2:
            flash("*First name must contain at least 2 characters!", 'register')
            is_valid = False
        if not fname.isalpha():
            flash("*First name must be letters only!", 'register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("*Last name must contain at least 2 characters!", 'register')
            is_valid = False
        if not lname.isalpha():
            flash("*Last name must be letters only!", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("*Invalid email address!", 'register')
            is_valid = False
        if user_in_db:
            flash("*Email already taken!", 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash("*Password must contain at least 8 characters!", 'register')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("*Passwords do not match!", 'register')
            is_valid = False
        return is_valid