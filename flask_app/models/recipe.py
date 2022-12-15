from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import database
from flask_app.models import user


class Recipe:
    def __init__(self,data):
        self.id=data['id']
        self.name=data['name']
        self.description=data['description']
        self.under_30mins=data['under_30mins']
        self.instructions=data['instructions']
        self.date=data['date']
        self.user_id=data['user_id']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def create(cls, data ):

        query = "INSERT INTO recipes ( name , description , under_30mins , instructions, date, user_id ) VALUES ( %(name)s , %(description)s , %(under_30mins)s , %(instructions)s, %(date)s, %(user_id)s );"

        return connectToMySQL(database).query_db( query, data )


    @classmethod
    def update(cls, data ):

        query = "UPDATE recipes set name=%(name)s , description=%(description)s , under_30mins=%(under_30mins)s , instructions=%(instructions)s, date=%(date)s where recipes.id=%(id)s;"

        return connectToMySQL(database).query_db( query, data )


    @classmethod
    def delete(cls, data ):

        query = "delete from recipes where recipes.id=%(id)s;"

        return connectToMySQL(database).query_db( query, data )

    @classmethod
    def get_all_recipes_with_user(cls):
        query="select * from recipes left join users on recipes.user_id=users.id;"
        results= connectToMySQL(database).query_db( query )
        all_recipes=[]
        if results:
            for row in results:
                this_recipe=cls(row)
                user_data={
                    **row,
                    'id':row['users.id'],
                    'created_at':row['users.created_at'],
                    'updated_at':row['users.updated_at']
                }
                this_user=user.User(user_data)
                this_recipe.created_by=this_user
                all_recipes.append(this_recipe)
        return all_recipes

    @classmethod
    def get_one_by_id(cls,data):
        query="select * from recipes left join users on recipes.user_id=users.id where recipes.id=%(id)s;"
        results= connectToMySQL(database).query_db( query,data )
        if results:
            row=results[0]
            this_recipe=cls(row)
            user_data={
                **row,
                'id':row['users.id'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at']
            }
            this_user=user.User(user_data)
            this_recipe.created_by=this_user
            return this_recipe
        return False #那页面会出现空白吗 还是页面崩了


    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(form_data['description']) < 3:
            flash("Description must be at least 3 characters.",)
            is_valid = False
        if len(form_data['instructions']) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False
        if len(form_data['date']) < 1:
            flash("Date must be filled.",)
            is_valid = False
        if 'under_30mins' not in form_data :
            flash("Under 30mins ?")
            is_valid = False
        return is_valid
